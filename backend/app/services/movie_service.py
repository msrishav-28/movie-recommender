"""
Movie Service - Business logic for movie operations.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
import logging

from app.db.models.movie import Movie
from app.schemas.movie import MovieSearch
from app.integrations.tmdb import get_tmdb_client
from app.cache.cache_manager import CacheManager

logger = logging.getLogger(__name__)


class MovieService:
    """Service for movie operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tmdb = get_tmdb_client()
        self.cache = CacheManager()
    
    async def get_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        """Get movie by ID."""
        cache_key = f"movie:{movie_id}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        movie = await self.db.get(Movie, movie_id)
        if movie:
            await self.cache.set(cache_key, movie, ttl=86400)
        return movie
    
    async def search_movies(self, search: MovieSearch, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Search movies with filters."""
        query = select(Movie)
        
        # Text search
        if search.query:
            query = query.where(
                or_(
                    Movie.title.ilike(f"%{search.query}%"),
                    Movie.overview.ilike(f"%{search.query}%")
                )
            )
        
        # Genre filter
        if search.genres:
            # Would filter by genre relationship
            pass
        
        # Year range
        if search.min_year or search.max_year:
            if search.min_year:
                query = query.where(func.extract('year', Movie.release_date) >= search.min_year)
            if search.max_year:
                query = query.where(func.extract('year', Movie.release_date) <= search.max_year)
        
        # Rating range
        if search.min_rating:
            query = query.where(Movie.vote_average >= search.min_rating)
        if search.max_rating:
            query = query.where(Movie.vote_average <= search.max_rating)
        
        # Sorting
        if search.sort_by == "popularity":
            query = query.order_by(Movie.popularity.desc() if search.sort_order == "desc" else Movie.popularity.asc())
        elif search.sort_by == "rating":
            query = query.order_by(Movie.vote_average.desc() if search.sort_order == "desc" else Movie.vote_average.asc())
        elif search.sort_by == "release_date":
            query = query.order_by(Movie.release_date.desc() if search.sort_order == "desc" else Movie.release_date.asc())
        else:
            query = query.order_by(Movie.title.asc())
        
        # Pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        result = await self.db.execute(query)
        movies = list(result.scalars().all())
        
        return {
            "movies": movies,
            "page": page,
            "page_size": page_size,
            "total": len(movies)  # Would get actual count
        }
    
    async def get_trending_movies(self, time_window: str = "week", limit: int = 20) -> List[Movie]:
        """Get trending movies."""
        cache_key = f"trending:{time_window}:{limit}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        # Get from TMDb API
        try:
            trending_data = await self.tmdb.get_trending_movies(time_window, limit)
            # Would sync with local database
            movies = []  # Convert from TMDb data
            await self.cache.set(cache_key, movies, ttl=300)
            return movies
        except Exception as e:
            logger.error(f"Failed to get trending movies: {e}")
            return []
