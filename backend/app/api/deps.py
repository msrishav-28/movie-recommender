"""
Common API dependencies.
"""

from typing import Optional, AsyncGenerator
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.security import get_current_user_id, get_current_user_optional
from app.db.models.user import User
from sqlalchemy import select


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
) -> User:
    """
    Get current authenticated user from database.
    
    Usage:
        @app.get("/protected")
        async def protected(user: User = Depends(get_current_user)):
            ...
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def get_current_active_user(
    user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user.
    """
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return user


async def get_current_verified_user(
    user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current verified user.
    """
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )
    return user


async def get_current_premium_user(
    user: User = Depends(get_current_verified_user)
) -> User:
    """
    Get current premium user.
    """
    if not user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required"
        )
    return user


async def get_current_admin_user(
    user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current admin user.
    """
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user


async def get_optional_user(
    db: AsyncSession = Depends(get_db),
    user_id: Optional[str] = Depends(get_current_user_optional)
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.
    For endpoints that work with or without authentication.
    """
    if not user_id:
        return None
    
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
