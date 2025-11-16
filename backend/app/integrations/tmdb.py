"""
TMDb (The Movie Database) API client.
Complete implementation for fetching movie metadata.
"""

import httpx
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

from app.core.config import settings
from app.core.exceptions import TMDbAPIError

logger = logging.getLogger(__name__)


class TMDbClient:
    """Client for TMDb API operations."""
    
    def __init__(self):
        self.base_url = settings.TMDB_BASE_URL
        self.api_key = settings.TMDB_API_KEY
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def _request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make API request to TMDb."""
        if params is None:
            params = {}
        
        params["api_key"] = self.api_key
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"TMDb API error: {e}")
            raise TMDbAPIError(f"Request failed: {e}")
    
    async def get_movie_details(self, movie_id: int) -> Dict[str, Any]:
        """
        Get detailed movie information.
        
        Args:
            movie_id: TMDb movie ID
        
        Returns:
            Movie details including genres, cast, crew, etc.
        """
        endpoint = f"movie/{movie_id}"
        params = {
            "append_to_response": "credits,keywords,videos,images,similar"
        }
        return await self._request(endpoint, params)
    
    async def search_movies(
        self,
        query: str,
        page: int = 1,
        year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Search for movies.
        
        Args:
            query: Search query
            page: Page number
            year: Optional year filter
        
        Returns:
            Search results
        """
        params = {
            "query": query,
            "page": page
        }
        if year:
            params["year"] = year
        
        return await self._request("search/movie", params)
    
    async def get_popular_movies(self, page: int = 1) -> Dict[str, Any]:
        """Get popular movies."""
        return await self._request("movie/popular", {"page": page})
    
    async def get_top_rated_movies(self, page: int = 1) -> Dict[str, Any]:
        """Get top rated movies."""
        return await self._request("movie/top_rated", {"page": page})
    
    async def get_now_playing(self, page: int = 1) -> Dict[str, Any]:
        """Get movies currently in theaters."""
        return await self._request("movie/now_playing", {"page": page})
    
    async def get_upcoming_movies(self, page: int = 1) -> Dict[str, Any]:
        """Get upcoming movies."""
        return await self._request("movie/upcoming", {"page": page})
    
    async def get_trending_movies(
        self,
        time_window: str = "week",
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Get trending movies.
        
        Args:
            time_window: "day" or "week"
            page: Page number
        """
        return await self._request(f"trending/movie/{time_window}", {"page": page})
    
    async def get_movie_credits(self, movie_id: int) -> Dict[str, Any]:
        """Get movie cast and crew."""
        return await self._request(f"movie/{movie_id}/credits")
    
    async def get_movie_keywords(self, movie_id: int) -> Dict[str, Any]:
        """Get movie keywords."""
        return await self._request(f"movie/{movie_id}/keywords")
    
    async def get_movie_videos(self, movie_id: int) -> Dict[str, Any]:
        """Get movie videos (trailers, teasers)."""
        return await self._request(f"movie/{movie_id}/videos")
    
    async def get_movie_images(self, movie_id: int) -> Dict[str, Any]:
        """Get movie images (posters, backdrops)."""
        return await self._request(f"movie/{movie_id}/images")
    
    async def get_similar_movies(
        self,
        movie_id: int,
        page: int = 1
    ) -> Dict[str, Any]:
        """Get movies similar to a specific movie."""
        return await self._request(f"movie/{movie_id}/similar", {"page": page})
    
    async def get_movie_recommendations(
        self,
        movie_id: int,
        page: int = 1
    ) -> Dict[str, Any]:
        """Get TMDb recommendations for a movie."""
        return await self._request(f"movie/{movie_id}/recommendations", {"page": page})
    
    async def get_person_details(self, person_id: int) -> Dict[str, Any]:
        """Get person (actor/director) details."""
        return await self._request(
            f"person/{person_id}",
            {"append_to_response": "movie_credits,tv_credits"}
        )
    
    async def get_genres(self) -> List[Dict[str, Any]]:
        """Get list of official genres."""
        response = await self._request("genre/movie/list")
        return response.get("genres", [])
    
    async def discover_movies(
        self,
        page: int = 1,
        sort_by: str = "popularity.desc",
        with_genres: Optional[List[int]] = None,
        year: Optional[int] = None,
        min_vote_average: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Discover movies with filters.
        
        Args:
            page: Page number
            sort_by: Sort method
            with_genres: Genre IDs to include
            year: Release year
            min_vote_average: Minimum rating
        """
        params = {
            "page": page,
            "sort_by": sort_by
        }
        
        if with_genres:
            params["with_genres"] = ",".join(map(str, with_genres))
        if year:
            params["year"] = year
        if min_vote_average:
            params["vote_average.gte"] = min_vote_average
        
        return await self._request("discover/movie", params)
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
    
    def get_image_url(self, path: str, size: str = "original") -> str:
        """
        Get full URL for TMDb image.
        
        Args:
            path: Image path from API response
            size: Image size (w500, original, etc.)
        """
        if not path:
            return ""
        return f"https://image.tmdb.org/t/p/{size}{path}"
    
    def get_youtube_url(self, key: str) -> str:
        """Get YouTube URL from video key."""
        return f"https://www.youtube.com/watch?v={key}"


# Singleton instance
_tmdb_client = None


def get_tmdb_client() -> TMDbClient:
    """Get singleton TMDb client."""
    global _tmdb_client
    if _tmdb_client is None:
        _tmdb_client = TMDbClient()
    return _tmdb_client
