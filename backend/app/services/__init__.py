"""
Services layer - Business logic for the application.
"""

from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.movie_service import MovieService
from app.services.rating_service import RatingService
from app.services.recommendation_service import RecommendationService
from app.services.watchlist_service import WatchlistService
from app.services.social_service import SocialService

__all__ = [
    "AuthService",
    "UserService",
    "MovieService",
    "RatingService",
    "RecommendationService",
    "WatchlistService",
    "SocialService",
]
