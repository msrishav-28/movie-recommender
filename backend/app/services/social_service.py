"""
Social Service - Business logic for social features.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from datetime import datetime
import logging

from app.db.models.user import UserFollow
from app.db.models.rating import Review
from app.core.exceptions import ValidationError, ResourceNotFoundError

logger = logging.getLogger(__name__)


class SocialService:
    """Service for social features."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def follow_user(self, follower_id: str, following_id: str):
        """Follow a user."""
        if follower_id == following_id:
            raise ValidationError("Cannot follow yourself")
        
        # Check if already following
        existing = await self.db.execute(
            select(UserFollow).where(
                UserFollow.follower_id == follower_id,
                UserFollow.following_id == following_id
            )
        )
        if existing.scalar_one_or_none():
            raise ValidationError("Already following this user")
        
        follow = UserFollow(
            follower_id=follower_id,
            following_id=following_id
        )
        self.db.add(follow)
        await self.db.commit()
        
        logger.info(f"User {follower_id} followed {following_id}")
    
    async def unfollow_user(self, follower_id: str, following_id: str):
        """Unfollow a user."""
        await self.db.execute(
            delete(UserFollow).where(
                UserFollow.follower_id == follower_id,
                UserFollow.following_id == following_id
            )
        )
        await self.db.commit()
        logger.info(f"User {follower_id} unfollowed {following_id}")
    
    async def get_followers(self, user_id: str) -> List[UserFollow]:
        """Get user's followers."""
        result = await self.db.execute(
            select(UserFollow).where(UserFollow.following_id == user_id)
        )
        return list(result.scalars().all())
    
    async def get_following(self, user_id: str) -> List[UserFollow]:
        """Get users that user is following."""
        result = await self.db.execute(
            select(UserFollow).where(UserFollow.follower_id == user_id)
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
    
    async def get_activity_feed(self, user_id: str, limit: int = 50) -> List[dict]:
        """Get activity feed for user (from followed users)."""
        # Get users that current user follows
        following_result = await self.db.execute(
            select(UserFollow.following_id).where(UserFollow.follower_id == user_id)
        )
        following_ids = [row[0] for row in following_result.all()]
        
        if not following_ids:
            return []
        
        # Get recent reviews from followed users
        reviews_result = await self.db.execute(
            select(Review)
            .where(Review.user_id.in_(following_ids))
            .where(Review.is_hidden == False)
            .order_by(Review.created_at.desc())
            .limit(limit)
        )
        reviews = reviews_result.scalars().all()
        
        # Convert to activity items
        activities = [
            {
                "id": review.id,
                "type": "review",
                "user_id": review.user_id,
                "movie_id": review.movie_id,
                "content": review.content,
                "created_at": review.created_at
            }
            for review in reviews
        ]
        
        return activities
    
    async def like_review(self, user_id: str, review_id: int):
        """Like a review."""
        # Would create ReviewLike record and increment counter
        logger.info(f"User {user_id} liked review {review_id}")
