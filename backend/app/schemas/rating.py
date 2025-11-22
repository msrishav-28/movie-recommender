"""
Rating and Review Pydantic schemas.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict
from datetime import datetime
from uuid import UUID

from app.schemas.common import TimestampMixin


class RatingCreate(BaseModel):
    """Schema for creating a rating."""
    movie_id: int
    overall_rating: float = Field(..., ge=0.0, le=5.0, description="Overall rating 0-5")
    plot_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    acting_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    cinematography_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    soundtrack_rating: Optional[float] = Field(None, ge=0.0, le=5.0)


class RatingUpdate(BaseModel):
    """Schema for updating a rating."""
    overall_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    plot_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    acting_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    cinematography_rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    soundtrack_rating: Optional[float] = Field(None, ge=0.0, le=5.0)


class RatingResponse(TimestampMixin):
    """Schema for rating response."""
    id: int
    user_id: UUID
    movie_id: int
    overall_rating: float
    plot_rating: Optional[float]
    acting_rating: Optional[float]
    cinematography_rating: Optional[float]
    soundtrack_rating: Optional[float]
    
    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    """Schema for creating a review."""
    movie_id: int
    rating_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=500)
    content: str = Field(..., min_length=10, max_length=5000)
    is_spoiler: bool = False


class ReviewUpdate(BaseModel):
    """Schema for updating a review."""
    title: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = Field(None, min_length=10, max_length=5000)
    is_spoiler: Optional[bool] = None


class ReviewResponse(TimestampMixin):
    """Schema for review response."""
    id: int
    user_id: UUID
    movie_id: int
    rating_id: Optional[int]
    title: Optional[str]
    content: str
    is_spoiler: bool
    
    # Sentiment analysis results
    sentiment_score: Optional[float]
    sentiment_label: Optional[str]
    sentiment_confidence: Optional[float]
    emotions: Optional[Dict[str, float]]
    aspect_sentiments: Optional[Dict[str, float]]
    
    # Engagement metrics
    likes_count: int
    comments_count: int
    helpful_count: int
    not_helpful_count: int
    
    # Moderation
    is_verified_watch: bool
    is_flagged: bool
    is_hidden: bool
    
    class Config:
        from_attributes = True


class ReviewWithUser(ReviewResponse):
    """Review response with user information."""
    username: str
    user_avatar: Optional[str]


class ReviewLikeRequest(BaseModel):
    """Schema for liking a review."""
    review_id: int


class ReviewCommentCreate(BaseModel):
    """Schema for creating a review comment."""
    review_id: int
    content: str = Field(..., min_length=1, max_length=1000)


class ReviewCommentResponse(TimestampMixin):
    """Schema for review comment response."""
    id: int
    review_id: int
    user_id: UUID
    content: str
    username: str
    user_avatar: Optional[str]
    is_flagged: bool
    is_hidden: bool
    
    class Config:
        from_attributes = True


class MovieRatingsAggregateResponse(BaseModel):
    """Schema for aggregated movie ratings."""
    movie_id: int
    avg_overall_rating: float
    avg_plot_rating: Optional[float]
    avg_acting_rating: Optional[float]
    avg_cinematography_rating: Optional[float]
    avg_soundtrack_rating: Optional[float]
    ratings_count: int
    rating_distribution: Dict[int, int]  # {1: 10, 2: 25, 3: 50, 4: 100, 5: 150}
