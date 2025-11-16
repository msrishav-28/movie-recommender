"""User management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from app.db.database import get_db
from app.db.models.user import User, UserPreferences
from app.api.deps import get_current_user, get_current_active_user

router = APIRouter()


class UserProfileResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    is_verified: bool
    is_premium: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class UserPreferencesResponse(BaseModel):
    favorite_genres: list[str]
    disliked_genres: list[str]
    diversity_preference: int
    profile_public: bool
    
    class Config:
        from_attributes = True


class UpdatePreferencesRequest(BaseModel):
    favorite_genres: Optional[list[str]] = None
    disliked_genres: Optional[list[str]] = None
    preferred_moods: Optional[list[str]] = None
    diversity_preference: Optional[int] = None
    profile_public: Optional[bool] = None


@router.get("/me/profile", response_model=UserProfileResponse)
async def get_my_profile(
    user: User = Depends(get_current_active_user)
):
    """Get current user's profile."""
    return user


@router.put("/me/profile", response_model=UserProfileResponse)
async def update_my_profile(
    data: UpdateProfileRequest,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user's profile."""
    
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.bio is not None:
        user.bio = data.bio
    if data.avatar_url is not None:
        user.avatar_url = data.avatar_url
    
    await db.commit()
    await db.refresh(user)
    
    return user


@router.get("/me/preferences", response_model=UserPreferencesResponse)
async def get_my_preferences(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's preferences."""
    
    result = await db.execute(
        select(UserPreferences).where(UserPreferences.user_id == user.id)
    )
    preferences = result.scalar_one_or_none()
    
    if not preferences:
        # Create default preferences
        preferences = UserPreferences(user_id=user.id)
        db.add(preferences)
        await db.commit()
        await db.refresh(preferences)
    
    return preferences


@router.put("/me/preferences", response_model=UserPreferencesResponse)
async def update_my_preferences(
    data: UpdatePreferencesRequest,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user's preferences."""
    
    result = await db.execute(
        select(UserPreferences).where(UserPreferences.user_id == user.id)
    )
    preferences = result.scalar_one_or_none()
    
    if not preferences:
        preferences = UserPreferences(user_id=user.id)
        db.add(preferences)
    
    if data.favorite_genres is not None:
        preferences.favorite_genres = data.favorite_genres
    if data.disliked_genres is not None:
        preferences.disliked_genres = data.disliked_genres
    if data.preferred_moods is not None:
        preferences.preferred_moods = data.preferred_moods
    if data.diversity_preference is not None:
        preferences.diversity_preference = data.diversity_preference
    if data.profile_public is not None:
        preferences.profile_public = data.profile_public
    
    await db.commit()
    await db.refresh(preferences)
    
    return preferences


@router.get("/{username}", response_model=UserProfileResponse)
async def get_user_profile(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    """Get public user profile by username."""
    
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if profile is public
    result = await db.execute(
        select(UserPreferences).where(UserPreferences.user_id == user.id)
    )
    preferences = result.scalar_one_or_none()
    
    if preferences and not preferences.profile_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Profile is private"
        )
    
    return user
