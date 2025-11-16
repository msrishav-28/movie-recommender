"""
API v1 Router - aggregates all endpoint routers.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    movies,
    recommendations,
    aesthetic_search,
    ratings,
    watchlist
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(movies.router, prefix="/movies", tags=["Movies"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(aesthetic_search.router, prefix="/aesthetic-search", tags=["Aesthetic Search"])
api_router.include_router(ratings.router, prefix="/ratings", tags=["Ratings & Reviews"])
api_router.include_router(watchlist.router, prefix="/watchlist", tags=["Watchlist"])
