"""
Repository layer - Data access pattern for clean separation.
"""

from app.db.repositories.user_repository import UserRepository
from app.db.repositories.movie_repository import MovieRepository
from app.db.repositories.rating_repository import RatingRepository
from app.db.repositories.watchlist_repository import WatchlistRepository

__all__ = [
    "UserRepository",
    "MovieRepository",
    "RatingRepository",
    "WatchlistRepository",
]
