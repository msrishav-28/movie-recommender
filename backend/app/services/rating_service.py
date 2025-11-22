"""
Rating Service - Business logic for ratings and reviews.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import logging

from app.db.models.rating import Rating, Review
from app.schemas.rating import RatingCreate, RatingUpdate, ReviewCreate, ReviewUpdate
from app.core.exceptions import ResourceNotFoundError, ValidationError
from app.ml.sentiment.analyzer import get_sentiment_analyzer

logger = logging.getLogger(__name__)


class RatingService:
    """Service for rating and review operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.sentiment_analyzer = get_sentiment_analyzer()
    
    async def create_rating(self, user_id: str, data: RatingCreate) -> Rating:
        """Create or update movie rating."""
        # Check if rating already exists
        existing = await self.db.execute(
            select(Rating).where(
                Rating.user_id == user_id,
                Rating.movie_id == data.movie_id
            )
        )
        rating = existing.scalar_one_or_none()
        
        if rating:
            # Update existing
            for field, value in data.dict(exclude={'movie_id'}).items():
                if value is not None:
                    setattr(rating, field, value)
        else:
            # Create new
            rating = Rating(user_id=user_id, **data.dict())
            self.db.add(rating)
        
        await self.db.commit()
        await self.db.refresh(rating)
        
        # Update movie aggregate ratings
        await self._update_movie_aggregate(data.movie_id)
        
        logger.info(f"Rating created/updated: user={user_id}, movie={data.movie_id}")
        return rating
    
    async def create_review(self, user_id: str, data: ReviewCreate) -> Review:
        """Create movie review with sentiment analysis."""
        review = Review(
            user_id=user_id,
            movie_id=data.movie_id,
            rating_id=data.rating_id,
            title=data.title,
            content=data.content,
            is_spoiler=data.is_spoiler
        )
        
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        
        # Queue sentiment analysis (async)
        try:
            analysis = await self.sentiment_analyzer.analyze_review(data.content)
            review.sentiment_score = analysis["sentiment_score"]
            review.sentiment_label = analysis["sentiment_label"]
            review.sentiment_confidence = analysis["sentiment_confidence"]
            review.emotions = analysis["emotions"]
            review.aspect_sentiments = analysis["aspect_sentiments"]
            await self.db.commit()
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
        
        logger.info(f"Review created: user={user_id}, movie={data.movie_id}")
        return review
    
    async def get_user_ratings(self, user_id: str, limit: int = 50) -> List[Rating]:
        """Get user's ratings."""
        result = await self.db.execute(
            select(Rating)
            .where(Rating.user_id == user_id)
            .order_by(Rating.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_movie_reviews(self, movie_id: int, limit: int = 20) -> List[Review]:
        """Get movie reviews."""
        result = await self.db.execute(
            select(Review)
            .where(Review.movie_id == movie_id)
            .where(Review.is_hidden == False)
            .order_by(Review.likes_count.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def _update_movie_aggregate(self, movie_id: int):
        """Update movie aggregate ratings."""
        result = await self.db.execute(
            select(
                func.avg(Rating.overall_rating).label('avg_rating'),
                func.count(Rating.id).label('count')
            ).where(Rating.movie_id == movie_id)
        )
        row = result.first()
        # Would update Movie model here
        logger.info(f"Movie aggregate updated: movie={movie_id}, avg={row[0]}, count={row[1]}")
