"""
Movie Repository - Data access for Movie models.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
import logging

from app.db.models.movie import Movie, Genre

logger = logging.getLogger(__name__)


class MovieRepository:
    """Repository for Movie data access."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, movie_id: int) -> Optional[Movie]:
        """Get movie by ID with all relationships."""
        result = await self.db.execute(
            select(Movie)
            .options(
                selectinload(Movie.genres),
                selectinload(Movie.cast),
                selectinload(Movie.crew)
            )
            .where(Movie.id == movie_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_ids(self, movie_ids: List[int]) -> List[Movie]:
        """Get multiple movies by IDs."""
        result = await self.db.execute(
            select(Movie)
            .where(Movie.id.in_(movie_ids))
        )
        return list(result.scalars().all())
    
    async def search(
        self,
        query: Optional[str] = None,
        genre_ids: Optional[List[int]] = None,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
        min_rating: Optional[float] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Movie]:
        """Search movies with filters."""
        stmt = select(Movie)
        
        # Text search
        if query:
            stmt = stmt.where(
                or_(
                    Movie.title.ilike(f"%{query}%"),
                    Movie.overview.ilike(f"%{query}%")
                )
            )
        
        # Year filters
        if min_year:
            stmt = stmt.where(func.extract('year', Movie.release_date) >= min_year)
        if max_year:
            stmt = stmt.where(func.extract('year', Movie.release_date) <= max_year)
        
        # Rating filter
        if min_rating:
            stmt = stmt.where(Movie.vote_average >= min_rating)
        
        # Pagination
        stmt = stmt.offset(offset).limit(limit)
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_popular(self, limit: int = 20) -> List[Movie]:
        """Get popular movies."""
        result = await self.db.execute(
            select(Movie)
            .order_by(Movie.popularity.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_top_rated(self, limit: int = 20, min_votes: int = 100) -> List[Movie]:
        """Get top rated movies."""
        result = await self.db.execute(
            select(Movie)
            .where(Movie.vote_count >= min_votes)
            .order_by(Movie.vote_average.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_by_genre(self, genre_id: int, limit: int = 20) -> List[Movie]:
        """Get movies by genre."""
        result = await self.db.execute(
            select(Movie)
            .join(Movie.genres)
            .where(Genre.id == genre_id)
            .order_by(Movie.popularity.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_recent_releases(self, limit: int = 20) -> List[Movie]:
        """Get recently released movies."""
        result = await self.db.execute(
            select(Movie)
            .where(Movie.release_date.isnot(None))
            .order_by(Movie.release_date.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_similar(self, movie_id: int, limit: int = 20) -> List[Movie]:
        """Get similar movies (by genre overlap)."""
        # Get source movie genres
        source_movie = await self.get_by_id(movie_id)
        if not source_movie or not source_movie.genres:
            return []
        
        genre_ids = [g.id for g in source_movie.genres]
        
        # Find movies with overlapping genres
        result = await self.db.execute(
            select(Movie)
            .join(Movie.genres)
            .where(Genre.id.in_(genre_ids))
            .where(Movie.id != movie_id)
            .group_by(Movie.id)
            .order_by(func.count(Genre.id).desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def update_aggregate_rating(self, movie_id: int, avg_rating: float, count: int):
        """Update movie's aggregate rating."""
        await self.db.execute(
            select(Movie)
            .where(Movie.id == movie_id)
        )
        # Would update aggregate fields here
        logger.info(f"Updated aggregate rating for movie {movie_id}: {avg_rating} ({count} ratings)")
    
    async def count(self) -> int:
        """Count total movies."""
        result = await self.db.execute(
            select(func.count(Movie.id))
        )
        return result.scalar_one()
