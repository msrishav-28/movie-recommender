"""Movie endpoints - search, get details, list movies."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

from app.db.database import get_db
from app.db.models.movie import Movie, Genre
from app.api.deps import get_optional_user

router = APIRouter()


class MovieResponse(BaseModel):
    id: int
    title: str
    original_title: Optional[str]
    overview: Optional[str]
    release_date: Optional[date]
    runtime: Optional[int]
    vote_average: Optional[float]
    popularity: Optional[float]
    poster_path: Optional[str]
    backdrop_path: Optional[str]
    genres: List[str] = []
    
    class Config:
        from_attributes = True


class MovieListResponse(BaseModel):
    movies: List[MovieResponse]
    total: int
    page: int
    page_size: int


@router.get("/search", response_model=MovieListResponse)
async def search_movies(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Search movies by title.
    """
    
    offset = (page - 1) * page_size
    
    # Search query
    search_query = select(Movie).where(
        or_(
            Movie.title.ilike(f"%{q}%"),
            Movie.original_title.ilike(f"%{q}%")
        )
    ).order_by(Movie.popularity.desc())
    
    # Count total
    count_query = select(func.count()).select_from(Movie).where(
        or_(
            Movie.title.ilike(f"%{q}%"),
            Movie.original_title.ilike(f"%{q}%")
        )
    )
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get paginated results
    result = await db.execute(search_query.offset(offset).limit(page_size))
    movies = result.scalars().all()
    
    return MovieListResponse(
        movies=[MovieResponse.from_orm(m) for m in movies],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/popular", response_model=MovieListResponse)
async def get_popular_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get popular movies.
    """
    
    offset = (page - 1) * page_size
    
    query = select(Movie).order_by(Movie.popularity.desc())
    count_query = select(func.count()).select_from(Movie)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    result = await db.execute(query.offset(offset).limit(page_size))
    movies = result.scalars().all()
    
    return MovieListResponse(
        movies=[MovieResponse.from_orm(m) for m in movies],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/trending", response_model=MovieListResponse)
async def get_trending_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get trending movies (placeholder - should use time-weighted popularity).
    """
    return await get_popular_movies(page, page_size, db)


@router.get("/top-rated", response_model=MovieListResponse)
async def get_top_rated_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get top rated movies (sorted by vote_average).
    """
    
    offset = (page - 1) * page_size
    
    query = select(Movie).where(Movie.vote_count >= 100).order_by(Movie.vote_average.desc())
    count_query = select(func.count()).select_from(Movie).where(Movie.vote_count >= 100)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    result = await db.execute(query.offset(offset).limit(page_size))
    movies = result.scalars().all()
    
    return MovieListResponse(
        movies=[MovieResponse.from_orm(m) for m in movies],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/upcoming", response_model=MovieListResponse)
async def get_upcoming_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get upcoming movies (release date in future).
    """
    from datetime import date as date_type
    
    offset = (page - 1) * page_size
    today = date_type.today()
    
    query = select(Movie).where(Movie.release_date > today).order_by(Movie.release_date.asc())
    count_query = select(func.count()).select_from(Movie).where(Movie.release_date > today)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    result = await db.execute(query.offset(offset).limit(page_size))
    movies = result.scalars().all()
    
    return MovieListResponse(
        movies=[MovieResponse.from_orm(m) for m in movies],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/genre/{genre_id}", response_model=MovieListResponse)
async def get_movies_by_genre(
    genre_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Get movies by genre.
    """
    
    offset = (page - 1) * page_size
    
    # This is a placeholder - actual implementation depends on genre relationship
    # Assuming genres are stored in a JSON field or separate table
    query = select(Movie).order_by(Movie.popularity.desc())
    count_query = select(func.count()).select_from(Movie)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    result = await db.execute(query.offset(offset).limit(page_size))
    movies = result.scalars().all()
    
    return MovieListResponse(
        movies=[MovieResponse.from_orm(m) for m in movies],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/genres")
async def get_all_genres(db: AsyncSession = Depends(get_db)):
    """
    Get all available genres.
    """
    
    result = await db.execute(select(Genre))
    genres = result.scalars().all()
    
    return [{"id": g.id, "name": g.name} for g in genres]


@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie_details(
    movie_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed movie information.
    """
    
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()
    
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    
    return MovieResponse.from_orm(movie)
