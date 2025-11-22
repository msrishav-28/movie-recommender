"""
Pydantic schemas for request/response validation.
"""

from app.schemas.user import *
from app.schemas.movie import *
from app.schemas.rating import *
from app.schemas.recommendation import *
from app.schemas.aesthetic import *
from app.schemas.watchlist import *
from app.schemas.social import *
from app.schemas.common import *

__all__ = [
    # User schemas
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenPayload",
    "UserPreferencesUpdate",
    "UserPreferencesResponse",
    
    # Movie schemas
    "MovieResponse",
    "MovieDetailResponse",
    "MovieSearch",
    "MovieFilter",
    
    # Rating schemas
    "RatingCreate",
    "RatingUpdate",
    "RatingResponse",
    "ReviewCreate",
    "ReviewUpdate",
    "ReviewResponse",
    
    # Recommendation schemas
    "RecommendationRequest",
    "RecommendationResponse",
    "RecommendationsListResponse",
    
    # Aesthetic search schemas
    "AestheticSearchRequest",
    "AestheticSearchResponse",
    "ColorPaletteRequest",
    
    # Watchlist schemas
    "WatchlistItemCreate",
    "WatchlistItemResponse",
    "WatchlistResponse",
    
    # Social schemas
    "UserFollowResponse",
    "UserListCreate",
    "UserListResponse",
    
    # Common schemas
    "PaginationParams",
    "PaginatedResponse",
    "SuccessResponse",
    "ErrorResponse",
]
