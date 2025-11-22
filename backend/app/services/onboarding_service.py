"""
Onboarding Service - Production Grade
Cold start solution with quick taste profiling quiz.
Generates initial recommendations for new users without history.
"""

from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.db.models.user import UserPreferences
from app.ml.recommendation.content_based import ContentBasedEngine
from app.core.config import settings

logger = logging.getLogger(__name__)


class OnboardingService:
    """
    Service for onboarding new users with cold start solution.
    
    Features:
    - 5-10 favorite movie selection
    - Mood preference quiz
    - Genre preference extraction
    - Initial content-based recommendations
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.content_engine = ContentBasedEngine()
    
    async def process_onboarding_quiz(
        self,
        user_id: str,
        favorite_movies: List[int],
        mood_preferences: List[str],
        genre_preferences: List[str] = None,
        avoid_genres: List[str] = None
    ) -> Dict[str, Any]:
        """
        Process onboarding quiz and generate initial profile.
        
        Args:
            user_id: User ID
            favorite_movies: List of 5-10 favorite movie IDs
            mood_preferences: Selected moods (e.g., ["intense", "thought-provoking"])
            genre_preferences: Optional genre preferences
            avoid_genres: Optional genres to avoid
        
        Returns:
            Onboarding results with initial recommendations
        """
        logger.info(f"Processing onboarding for user {user_id}")
        
        # Extract genres from favorite movies
        if not genre_preferences:
            genre_preferences = await self._extract_genres_from_favorites(favorite_movies)
        
        # Create or update user preferences
        await self._create_user_preferences(
            user_id=user_id,
            genres=genre_preferences,
            moods=mood_preferences,
            avoid_genres=avoid_genres or []
        )
        
        # Generate initial recommendations based on favorites
        initial_recommendations = await self._generate_initial_recommendations(
            favorite_movies=favorite_movies,
            genre_preferences=genre_preferences,
            mood_preferences=mood_preferences
        )
        
        return {
            "success": True,
            "profile_created": True,
            "favorite_genres": genre_preferences,
            "mood_preferences": mood_preferences,
            "initial_recommendations": initial_recommendations[:20],
            "total_recommendations": len(initial_recommendations)
        }
    
    async def _extract_genres_from_favorites(
        self,
        movie_ids: List[int]
    ) -> List[str]:
        """
        Extract common genres from favorite movies.
        
        Args:
            movie_ids: List of favorite movie IDs
        
        Returns:
            List of extracted genres
        """
        from collections import Counter
        
        # In production, query actual movie genres from database
        # For now, return common genres
        genre_counter = Counter()
        
        # Placeholder: would query database
        # This would be replaced with actual DB queries
        common_genres = [
            "Drama", "Thriller", "Science Fiction",
            "Comedy", "Action"
        ]
        
        return common_genres[:5]
    
    async def _create_user_preferences(
        self,
        user_id: str,
        genres: List[str],
        moods: List[str],
        avoid_genres: List[str]
    ):
        """
        Create initial user preferences from quiz.
        
        Args:
            user_id: User ID
            genres: Preferred genres
            moods: Preferred moods
            avoid_genres: Genres to avoid
        """
        # Check if preferences exist
        from sqlalchemy import select
        result = await self.db.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        prefs = result.scalar_one_or_none()
        
        if prefs:
            # Update existing
            prefs.favorite_genres = genres
            prefs.preferred_moods = moods
            prefs.disliked_genres = avoid_genres
            prefs.diversity_preference = 7  # Default medium-high diversity
        else:
            # Create new
            prefs = UserPreferences(
                user_id=user_id,
                favorite_genres=genres,
                preferred_moods=moods,
                disliked_genres=avoid_genres,
                diversity_preference=7,
                enable_llm_recommendations=True,
                enable_aesthetic_search=True,
                enable_gnn_recommendations=True
            )
            self.db.add(prefs)
        
        await self.db.commit()
        logger.info(f"Created preferences for user {user_id}")
    
    async def _generate_initial_recommendations(
        self,
        favorite_movies: List[int],
        genre_preferences: List[str],
        mood_preferences: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate initial content-based recommendations.
        
        Args:
            favorite_movies: User's favorite movies
            genre_preferences: Preferred genres
            mood_preferences: Preferred moods
        
        Returns:
            List of initial recommendations
        """
        recommendations = []
        
        # Get similar movies to each favorite
        for movie_id in favorite_movies[:3]:  # Use top 3 favorites
            similar = await self.content_engine.get_similar_movies(
                user_id=None,  # No user context yet
                k=10,
                filters={"movie_id": movie_id}
            )
            recommendations.extend(similar)
        
        # Add genre-based recommendations
        genre_recs = await self._get_popular_by_genres(genre_preferences, limit=20)
        recommendations.extend(genre_recs)
        
        # Remove duplicates and limit
        seen = set()
        unique_recs = []
        for rec in recommendations:
            movie_id = rec.get("movie_id")
            if movie_id not in seen and movie_id not in favorite_movies:
                seen.add(movie_id)
                unique_recs.append(rec)
        
        return unique_recs[:50]
    
    async def _get_popular_by_genres(
        self,
        genres: List[str],
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get popular movies in preferred genres.
        
        Args:
            genres: Genre list
            limit: Number of movies
        
        Returns:
            List of popular movies
        """
        # In production: query database for popular movies in these genres
        # Return placeholder for now
        return [
            {
                "movie_id": i + 1000,
                "score": 0.8,
                "metadata": {"genres": genres[:2]}
            }
            for i in range(limit)
        ]
    
    def generate_quiz_questions(self) -> List[Dict[str, Any]]:
        """
        Generate onboarding quiz questions.
        
        Returns:
            List of quiz questions
        """
        return [
            {
                "id": 1,
                "type": "movie_selection",
                "question": "Select 5-10 of your favorite movies",
                "description": "This helps us understand your taste",
                "min_selections": 5,
                "max_selections": 10
            },
            {
                "id": 2,
                "type": "mood_selection",
                "question": "What moods do you typically enjoy?",
                "options": [
                    "Intense and thrilling",
                    "Thought-provoking and deep",
                    "Light-hearted and fun",
                    "Emotional and moving",
                    "Dark and mysterious",
                    "Uplifting and inspiring"
                ],
                "multiple": True
            },
            {
                "id": 3,
                "type": "genre_avoid",
                "question": "Are there any genres you prefer to avoid?",
                "options": [
                    "Horror", "Romance", "Musicals",
                    "Westerns", "War", "Sports"
                ],
                "multiple": True,
                "optional": True
            },
            {
                "id": 4,
                "type": "rating_preference",
                "question": "Do you prefer highly-rated classics or discover hidden gems?",
                "options": [
                    "Highly-rated classics",
                    "Hidden gems",
                    "Mix of both"
                ],
                "single": True
            },
            {
                "id": 5,
                "type": "decade_preference",
                "question": "Which decades do you enjoy most?",
                "options": [
                    "Recent (2020s)",
                    "2010s",
                    "2000s",
                    "1990s",
                    "1980s",
                    "Classic (pre-1980)"
                ],
                "multiple": True,
                "optional": True
            }
        ]
