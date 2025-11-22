"""
User Repository - Data access for User models.
"""

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
import logging

from app.db.models.user import User, UserPreferences, UserFollow

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for User data access."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user: User) -> User:
        """Create a new user."""
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.preferences))
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def update(self, user_id: str, data: dict) -> Optional[User]:
        """Update user."""
        result = await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**data)
            .returning(User)
        )
        await self.db.commit()
        return result.scalar_one_or_none()
    
    async def delete(self, user_id: str) -> bool:
        """Delete user."""
        result = await self.db.execute(
            delete(User).where(User.id == user_id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def get_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """Get user preferences."""
        result = await self.db.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update_preferences(self, user_id: str, data: dict) -> UserPreferences:
        """Update user preferences."""
        # Check if preferences exist
        prefs = await self.get_preferences(user_id)
        
        if prefs:
            # Update existing
            for key, value in data.items():
                setattr(prefs, key, value)
        else:
            # Create new
            prefs = UserPreferences(user_id=user_id, **data)
            self.db.add(prefs)
        
        await self.db.commit()
        await self.db.refresh(prefs)
        return prefs
    
    async def get_followers(self, user_id: str) -> List[User]:
        """Get user's followers."""
        result = await self.db.execute(
            select(User)
            .join(UserFollow, UserFollow.follower_id == User.id)
            .where(UserFollow.following_id == user_id)
        )
        return list(result.scalars().all())
    
    async def get_following(self, user_id: str) -> List[User]:
        """Get users that user is following."""
        result = await self.db.execute(
            select(User)
            .join(UserFollow, UserFollow.following_id == User.id)
            .where(UserFollow.follower_id == user_id)
        )
        return list(result.scalars().all())
    
    async def is_following(self, follower_id: str, following_id: str) -> bool:
        """Check if user is following another user."""
        result = await self.db.execute(
            select(UserFollow).where(
                UserFollow.follower_id == follower_id,
                UserFollow.following_id == following_id
            )
        )
        return result.scalar_one_or_none() is not None
    
    async def search(self, query: str, limit: int = 20) -> List[User]:
        """Search users by username or email."""
        result = await self.db.execute(
            select(User)
            .where(
                (User.username.ilike(f"%{query}%")) |
                (User.email.ilike(f"%{query}%"))
            )
            .limit(limit)
        )
        return list(result.scalars().all())
