"""
Movie-related Pydantic schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date

from app.schemas.common import TimestampMixin, PaginationParams


class GenreResponse(BaseModel):
    """Schema for genre."""
    id: int
    name: str
    
    class Config:
        from_attributes = True


class CastMemberResponse(BaseModel):
    """Schema for cast member."""
    id: int
    name: str
    character: Optional[str]
    profile_path: Optional[str]
    order: int
    
    class Config:
        from_attributes = True


class CrewMemberResponse(BaseModel):
    """Schema for crew member."""
    id: int
    name: str
    job: str
    department: str
    profile_path: Optional[str]
    
    class Config:
        from_attributes = True


class MovieResponse(BaseModel):
    """Basic movie response schema."""
    id: int
    title: str
    original_title: Optional[str]
    overview: Optional[str]
    release_date: Optional[date]
    poster_path: Optional[str]
    backdrop_path: Optional[str]
    genres: List[GenreResponse] = []
    vote_average: Optional[float]
    vote_count: int
    popularity: float
    runtime: Optional[int]
    
    class Config:
        from_attributes = True


class MovieDetailResponse(MovieResponse):
    """Detailed movie response with all information."""
    tagline: Optional[str]
    budget: Optional[int]
    revenue: Optional[int]
    original_language: str
    spoken_languages: List[str] = []
    production_countries: List[str] = []
    cast: List[CastMemberResponse] = []
    crew: List[CrewMemberResponse] = []
    trailer_url: Optional[str]
    imdb_id: Optional[str]
    homepage: Optional[str]
    status: Optional[str]
    
    # Aggregated ratings
    avg_rating: Optional[float]
    ratings_count: int = 0
    
    # Sentiment data
    avg_sentiment: Optional[float]
    sentiment_distribution: Optional[Dict[str, int]]
    
    class Config:
        from_attributes = True


class MovieSearch(BaseModel):
    """Schema for movie search parameters."""
    query: Optional[str] = Field(None, min_length=1)
    genres: Optional[List[str]] = None
    min_year: Optional[int] = Field(None, ge=1900, le=2100)
    max_year: Optional[int] = Field(None, ge=1900, le=2100)
    min_rating: Optional[float] = Field(None, ge=0, le=10)
    max_rating: Optional[float] = Field(None, ge=0, le=10)
    min_runtime: Optional[int] = Field(None, ge=0)
    max_runtime: Optional[int] = Field(None, ge=0)
    languages: Optional[List[str]] = None
    sort_by: Optional[str] = Field("popularity", pattern=r'^(popularity|rating|release_date|title)$')
    sort_order: Optional[str] = Field("desc", pattern=r'^(asc|desc)$')


class MovieFilter(PaginationParams):
    """Schema for filtering movies."""
    genre_ids: Optional[List[int]] = None
    year: Optional[int] = None
    min_rating: Optional[float] = None
    language: Optional[str] = None


class StreamingAvailability(BaseModel):
    """Schema for streaming availability."""
    service_name: str
    service_id: str
    link: Optional[str]
    quality: Optional[str]
    price: Optional[float]
    currency: Optional[str]
    
    class Config:
        from_attributes = True


class MovieWithAvailability(MovieResponse):
    """Movie response with streaming availability."""
    streaming_services: List[StreamingAvailability] = []
