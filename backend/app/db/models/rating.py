"""
Rating and Review models with sentiment analysis.
"""

from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, Index, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class Rating(Base):
    """Multi-dimensional movie ratings."""
    
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Overall rating (required)
    overall_rating = Column(Float, nullable=False)  # 0-5 scale
    
    # Multi-dimensional ratings (optional)
    plot_rating = Column(Float)  # 0-5
    acting_rating = Column(Float)  # 0-5
    cinematography_rating = Column(Float)  # 0-5
    soundtrack_rating = Column(Float)  # 0-5
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
    review = relationship("Review", back_populates="rating", uselist=False)
    
    # Constraints and indexes
    __table_args__ = (
        Index('idx_rating_user', 'user_id'),
        Index('idx_rating_movie', 'movie_id'),
        Index('idx_rating_overall', 'overall_rating'),
        Index('idx_rating_created', 'created_at'),
        # Unique constraint: one rating per user per movie
        Index('idx_rating_unique', 'user_id', 'movie_id', unique=True),
    )
    
    def __repr__(self):
        return f"<Rating user={self.user_id} movie={self.movie_id} rating={self.overall_rating}>"


class Review(Base):
    """User reviews with sentiment analysis."""
    
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    rating_id = Column(Integer, ForeignKey("ratings.id", ondelete="CASCADE"), unique=True)
    
    # Review content
    title = Column(String(500))
    content = Column(Text, nullable=False)
    
    # Sentiment analysis results
    sentiment_score = Column(Float)  # -1 (negative) to 1 (positive)
    sentiment_label = Column(String(20))  # positive, negative, neutral
    sentiment_confidence = Column(Float)  # 0-1
    
    # Emotion detection
    emotions = Column(JSONB)  # {joy: 0.8, anger: 0.1, sadness: 0.3, ...}
    
    # Aspect-based sentiment
    aspect_sentiments = Column(JSONB)  # {plot: 0.7, acting: 0.9, cinematography: 0.5}
    
    # Moderation and quality
    is_spoiler = Column(Boolean, default=False)
    is_verified_watch = Column(Boolean, default=False)  # User actually watched the movie
    helpful_count = Column(Integer, default=0)
    not_helpful_count = Column(Integer, default=0)
    report_count = Column(Integer, default=0)
    is_flagged = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
    
    # Engagement
    likes_count = Column(Integer, default=0, index=True)
    comments_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    sentiment_analyzed_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")
    rating = relationship("Rating", back_populates="review")
    likes = relationship("ReviewLike", back_populates="review", cascade="all, delete-orphan")
    comments = relationship("ReviewComment", back_populates="review", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_review_user', 'user_id'),
        Index('idx_review_movie', 'movie_id'),
        Index('idx_review_likes', 'likes_count'),
        Index('idx_review_created', 'created_at'),
        Index('idx_review_sentiment', 'sentiment_score'),
    )
    
    def __repr__(self):
        return f"<Review id={self.id} movie={self.movie_id}>"


class ReviewLike(Base):
    """Likes on reviews."""
    
    __tablename__ = "review_likes"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), primary_key=True)
    
    liked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User")
    review = relationship("Review", back_populates="likes")
    
    __table_args__ = (
        Index('idx_review_like_user', 'user_id'),
        Index('idx_review_like_review', 'review_id'),
    )


class ReviewComment(Base):
    """Comments on reviews."""
    
    __tablename__ = "review_comments"
    
    id = Column(Integer, primary_key=True)
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    content = Column(Text, nullable=False)
    
    is_flagged = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    review = relationship("Review", back_populates="comments")
    user = relationship("User")
    
    __table_args__ = (
        Index('idx_comment_review', 'review_id'),
        Index('idx_comment_user', 'user_id'),
        Index('idx_comment_created', 'created_at'),
    )


class MovieRecommendation(Base):
    """Cached recommendations for users."""
    
    __tablename__ = "movie_recommendations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Recommendation metadata
    score = Column(Float, nullable=False)
    rank = Column(Integer)  # Position in recommendation list
    
    # Component scores
    collaborative_score = Column(Float)
    content_score = Column(Float)
    gnn_score = Column(Float)
    sentiment_score = Column(Float)
    popularity_score = Column(Float)
    context_score = Column(Float)
    
    # Explanation
    explanation = Column(Text)
    confidence = Column(Float)
    
    # Source algorithm
    algorithm_version = Column(String(50))
    
    # Timestamps
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    __table_args__ = (
        Index('idx_recommendation_user', 'user_id'),
        Index('idx_recommendation_score', 'score'),
        Index('idx_recommendation_generated', 'generated_at'),
        Index('idx_recommendation_expires', 'expires_at'),
    )
