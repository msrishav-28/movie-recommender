"""
User Service - Business logic for user operations.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import logging

from app.db.models.user import User, UserPreferences
from app.schemas.user import UserUpdate, UserPreferencesUpdate
from app.core.exceptions import ResourceNotFoundError
from app.cache.cache_manager import CacheManager

logger = logging.getLogger(__name__)


class UserService:
    """Service for user operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.cache = CacheManager()
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        # Try cache first
        cached = await self.cache.get(f"user:{user_id}")
        if cached:
            return cached
        
        user = await self.db.get(User, user_id)
        if user:
            await self.cache.set(f"user:{user_id}", user, ttl=1800)
        return user
    
    async def update_user(self, user_id: str, data: UserUpdate) -> User:
        """Update user profile."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundError("User", user_id)
        
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        await self.cache.delete(f"user:{user_id}")
        
        logger.info(f"User updated: {user_id}")
        return user
    
    async def get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """Get user preferences."""
        result = await self.db.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update_user_preferences(self, user_id: str, data: UserPreferencesUpdate) -> UserPreferences:
        """Update user preferences."""
        prefs = await self.get_user_preferences(user_id)
        
        if not prefs:
            # Create new preferences
            prefs = UserPreferences(user_id=user_id)
            self.db.add(prefs)
        
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(prefs, field, value)
        
        await self.db.commit()
        await self.db.refresh(prefs)
        
        logger.info(f"User preferences updated: {user_id}")
        return prefs
