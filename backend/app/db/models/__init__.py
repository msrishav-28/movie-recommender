"""Database models package."""

from app.db.models.user import (
    User,
    UserPreferences,
    UserFollow,
    UserAPIKey,
    UserSession
)
from app.db.models.movie import (
    Movie,
    Genre,
    Keyword,
    Person,
    MovieCast,
    MovieCrew,
    Collection,
    ProductionCompany,
    Country,
    Language
)
from app.db.models.rating import (
    Rating,
    Review,
    ReviewLike,
    ReviewComment,
    MovieRecommendation
)
from app.db.models.watchlist import (
    WatchlistItem,
    UserList,
    ListItem,
    ListCollaborator,
    ListLike,
    WatchHistory
)

__all__ = [
    # User models
    "User",
    "UserPreferences",
    "UserFollow",
    "UserAPIKey",
    "UserSession",
    # Movie models
    "Movie",
    "Genre",
    "Keyword",
    "Person",
    "MovieCast",
    "MovieCrew",
    "Collection",
    "ProductionCompany",
    "Country",
    "Language",
    # Rating models
    "Rating",
    "Review",
    "ReviewLike",
    "ReviewComment",
    "MovieRecommendation",
    # Watchlist models
    "WatchlistItem",
    "UserList",
    "ListItem",
    "ListCollaborator",
    "ListLike",
    "WatchHistory",
]
