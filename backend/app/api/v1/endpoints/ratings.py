"""Ratings and reviews endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.db.database import get_db
from app.db.models.rating import Rating, Review
from app.db.models.user import User
from app.api.deps import get_current_active_user

router = APIRouter()


class CreateRatingRequest(BaseModel):
    movie_id: int
    overall_rating: float = Field(..., ge=0, le=5)
    plot_rating: Optional[float] = Field(None, ge=0, le=5)
    acting_rating: Optional[float] = Field(None, ge=0, le=5)
    cinematography_rating: Optional[float] = Field(None, ge=0, le=5)
    soundtrack_rating: Optional[float] = Field(None, ge=0, le=5)


class RatingResponse(BaseModel):
    id: int
    movie_id: int
    overall_rating: float
    plot_rating: Optional[float]
    acting_rating: Optional[float]
    cinematography_rating: Optional[float]
    soundtrack_rating: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


class CreateReviewRequest(BaseModel):
    movie_id: int
    rating_id: int
    title: Optional[str] = Field(None, max_length=500)
    content: str = Field(..., min_length=10)
    is_spoiler: bool = False


class ReviewResponse(BaseModel):
    id: int
    movie_id: int
    title: Optional[str]
    content: str
    sentiment_score: Optional[float]
    sentiment_label: Optional[str]
    is_spoiler: bool
    likes_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/rate", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
async def rate_movie(
    data: CreateRatingRequest,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Rate a movie (creates or updates rating).
    
    Multi-dimensional ratings:
    - Overall rating (required): 0-5
    - Plot rating (optional): 0-5
    - Acting rating (optional): 0-5
    - Cinematography rating (optional): 0-5
    - Soundtrack rating (optional): 0-5
    """
    
    # Check if rating already exists
    result = await db.execute(
        select(Rating).where(
            Rating.user_id == user.id,
            Rating.movie_id == data.movie_id
        )
    )
    rating = result.scalar_one_or_none()
    
    if rating:
        # Update existing rating
        rating.overall_rating = data.overall_rating
        rating.plot_rating = data.plot_rating
        rating.acting_rating = data.acting_rating
        rating.cinematography_rating = data.cinematography_rating
        rating.soundtrack_rating = data.soundtrack_rating
    else:
        # Create new rating
        rating = Rating(
            user_id=user.id,
            movie_id=data.movie_id,
            overall_rating=data.overall_rating,
            plot_rating=data.plot_rating,
            acting_rating=data.acting_rating,
            cinematography_rating=data.cinematography_rating,
            soundtrack_rating=data.soundtrack_rating
        )
        db.add(rating)
    
    await db.commit()
    await db.refresh(rating)
    
    # TODO: Update movie aggregate ratings
    # await update_movie_ratings(db, data.movie_id)
    
    return rating


@router.get("/my-ratings", response_model=List[RatingResponse])
async def get_my_ratings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's ratings."""
    
    offset = (page - 1) * page_size
    
    result = await db.execute(
        select(Rating)
        .where(Rating.user_id == user.id)
        .order_by(Rating.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    ratings = result.scalars().all()
    
    return [RatingResponse.from_orm(r) for r in ratings]


@router.post("/review", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    data: CreateReviewRequest,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a review for a movie.
    
    - Must have rated the movie first
    - Content min 10 characters
    - Mark as spoiler if necessary
    """
    
    # Verify rating exists and belongs to user
    result = await db.execute(
        select(Rating).where(
            Rating.id == data.rating_id,
            Rating.user_id == user.id
        )
    )
    rating = result.scalar_one_or_none()
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found or doesn't belong to you"
        )
    
    # Check if review already exists
    result = await db.execute(
        select(Review).where(Review.rating_id == data.rating_id)
    )
    existing_review = result.scalar_one_or_none()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Review already exists for this rating"
        )
    
    # Create review
    review = Review(
        user_id=user.id,
        movie_id=data.movie_id,
        rating_id=data.rating_id,
        title=data.title,
        content=data.content,
        is_spoiler=data.is_spoiler
    )
    
    db.add(review)
    await db.commit()
    await db.refresh(review)
    
    # TODO: Queue sentiment analysis
    # from app.workers.tasks.sentiment_analysis import analyze_review
    # analyze_review.delay(review.id)
    
    return review


@router.get("/movie/{movie_id}/reviews", response_model=List[ReviewResponse])
async def get_movie_reviews(
    movie_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get reviews for a movie."""
    
    offset = (page - 1) * page_size
    
    result = await db.execute(
        select(Review)
        .where(Review.movie_id == movie_id)
        .order_by(Review.likes_count.desc(), Review.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    reviews = result.scalars().all()
    
    return [ReviewResponse.from_orm(r) for r in reviews]


@router.post("/review/{review_id}/like")
async def like_review(
    review_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Like a review."""
    
    # TODO: Implement review likes
    # from app.db.models.rating import ReviewLike
    # Check if already liked, if not create like and increment count
    
    return {"status": "liked"}


@router.delete("/rating/{rating_id}")
async def delete_rating(
    rating_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a rating (and associated review)."""
    
    result = await db.execute(
        select(Rating).where(
            Rating.id == rating_id,
            Rating.user_id == user.id
        )
    )
    rating = result.scalar_one_or_none()
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    await db.delete(rating)
    await db.commit()
    
    return {"status": "deleted"}
