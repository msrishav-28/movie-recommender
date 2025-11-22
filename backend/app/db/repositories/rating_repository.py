"""
Rating Repository - Data access for Rating and Review models.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from datetime import datetime
import logging

from app.db.models.rating import Rating, Review, ReviewLike

logger = logging.getLogger(__name__)


class RatingRepository:
    """Repository for Rating and Review data access."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # Rating operations
    async def create_rating(self, rating: Rating) -> Rating:
        """Create a new rating."""
        self.db.add(rating)
        await self.db.commit()
        await self.db.refresh(rating)
        return rating
    
    async def get_rating(self, user_id: str, movie_id: int) -> Optional[Rating]:
        """Get user's rating for a movie."""
        result = await self.db.execute(
            select(Rating).where(
                Rating.user_id == user_id,
                Rating.movie_id == movie_id
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_ratings(self, user_id: str, limit: int = 50, offset: int = 0) -> List[Rating]:
        """Get all ratings by user."""
        result = await self.db.execute(
            select(Rating)
            .where(Rating.user_id == user_id)
            .order_by(Rating.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_movie_ratings(self, movie_id: int, limit: int = 100) -> List[Rating]:
        """Get all ratings for a movie."""
        result = await self.db.execute(
            select(Rating)
            .where(Rating.movie_id == movie_id)
            .order_by(Rating.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def update_rating(self, rating_id: int, data: dict) -> Optional[Rating]:
        """Update a rating."""
        result = await self.db.execute(
            select(Rating).where(Rating.id == rating_id)
        )
        rating = result.scalar_one_or_none()
        
        if rating:
            for key, value in data.items():
                setattr(rating, key, value)
            await self.db.commit()
            await self.db.refresh(rating)
        
        return rating
    
    async def delete_rating(self, rating_id: int) -> bool:
        """Delete a rating."""
        result = await self.db.execute(
            delete(Rating).where(Rating.id == rating_id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def get_movie_rating_stats(self, movie_id: int) -> Dict[str, Any]:
        """Get aggregate rating statistics for a movie."""
        result = await self.db.execute(
            select(
                func.avg(Rating.overall_rating).label('avg_overall'),
                func.avg(Rating.plot_rating).label('avg_plot'),
                func.avg(Rating.acting_rating).label('avg_acting'),
                func.avg(Rating.cinematography_rating).label('avg_cinematography'),
                func.avg(Rating.soundtrack_rating).label('avg_soundtrack'),
                func.count(Rating.id).label('count')
            ).where(Rating.movie_id == movie_id)
        )
        row = result.first()
        
        return {
            "avg_overall_rating": float(row.avg_overall) if row.avg_overall else None,
            "avg_plot_rating": float(row.avg_plot) if row.avg_plot else None,
            "avg_acting_rating": float(row.avg_acting) if row.avg_acting else None,
            "avg_cinematography_rating": float(row.avg_cinematography) if row.avg_cinematography else None,
            "avg_soundtrack_rating": float(row.avg_soundtrack) if row.avg_soundtrack else None,
            "ratings_count": row.count
        }
    
    # Review operations
    async def create_review(self, review: Review) -> Review:
        """Create a new review."""
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review
    
    async def get_review(self, review_id: int) -> Optional[Review]:
        """Get review by ID."""
        result = await self.db.execute(
            select(Review).where(Review.id == review_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_reviews(self, user_id: str, limit: int = 20, offset: int = 0) -> List[Review]:
        """Get user's reviews."""
        result = await self.db.execute(
            select(Review)
            .where(Review.user_id == user_id)
            .where(Review.is_hidden == False)
            .order_by(Review.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_movie_reviews(
        self,
        movie_id: int,
        limit: int = 20,
        offset: int = 0,
        sort_by: str = "likes"
    ) -> List[Review]:
        """Get reviews for a movie."""
        stmt = select(Review).where(
            Review.movie_id == movie_id,
            Review.is_hidden == False
        )
        
        if sort_by == "likes":
            stmt = stmt.order_by(Review.likes_count.desc())
        elif sort_by == "recent":
            stmt = stmt.order_by(Review.created_at.desc())
        else:
            stmt = stmt.order_by(Review.created_at.desc())
        
        stmt = stmt.offset(offset).limit(limit)
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def update_review(self, review_id: int, data: dict) -> Optional[Review]:
        """Update a review."""
        result = await self.db.execute(
            select(Review).where(Review.id == review_id)
        )
        review = result.scalar_one_or_none()
        
        if review:
            for key, value in data.items():
                setattr(review, key, value)
            await self.db.commit()
            await self.db.refresh(review)
        
        return review
    
    async def delete_review(self, review_id: int) -> bool:
        """Delete a review."""
        result = await self.db.execute(
            delete(Review).where(Review.id == review_id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def increment_review_likes(self, review_id: int):
        """Increment review like count."""
        result = await self.db.execute(
            select(Review).where(Review.id == review_id)
        )
        review = result.scalar_one_or_none()
        
        if review:
            review.likes_count += 1
            await self.db.commit()
    
    async def decrement_review_likes(self, review_id: int):
        """Decrement review like count."""
        result = await self.db.execute(
            select(Review).where(Review.id == review_id)
        )
        review = result.scalar_one_or_none()
        
        if review:
            review.likes_count = max(0, review.likes_count - 1)
            await self.db.commit()
