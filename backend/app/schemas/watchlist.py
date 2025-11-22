"""
Watchlist Pydantic schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.schemas.common import TimestampMixin
from app.schemas.movie import MovieResponse


class WatchlistItemCreate(BaseModel):
    """Schema for adding item to watchlist."""
    movie_id: int
    priority: Optional[int] = Field(None, ge=1, le=5, description="Priority level 1-5")
    notes: Optional[str] = Field(None, max_length=500)


class WatchlistItemUpdate(BaseModel):
    """Schema for updating watchlist item."""
    priority: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = Field(None, max_length=500)
    watched: Optional[bool] = None


class WatchlistItemResponse(TimestampMixin):
    """Schema for watchlist item response."""
    id: int
    user_id: UUID
    movie_id: int
    priority: Optional[int]
    notes: Optional[str]
    watched: bool
    watched_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class WatchlistItemWithMovie(WatchlistItemResponse):
    """Watchlist item with full movie details."""
    movie: MovieResponse


class WatchlistResponse(BaseModel):
    """Schema for watchlist response."""
    items: List[WatchlistItemWithMovie]
    total_count: int
    watched_count: int
    unwatched_count: int


class WatchlistStats(BaseModel):
    """Schema for watchlist statistics."""
    total_items: int
    watched: int
    unwatched: int
    avg_priority: Optional[float]
    genre_distribution: dict
    decade_distribution: dict


class BulkWatchlistOperation(BaseModel):
    """Schema for bulk watchlist operations."""
    movie_ids: List[int] = Field(..., min_items=1, max_items=50)
    operation: str = Field(..., pattern=r'^(add|remove|mark_watched)$')
