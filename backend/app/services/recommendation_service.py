"""
Recommendation Service - Business logic for recommendations.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.ml.recommendation.hybrid_engine import get_recommendation_engine, RecommendationRequest
from app.schemas.recommendation import RecommendationResponse
from app.core.exceptions import MLModelError

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for movie recommendations."""
    
    def __init__(self, db: AsyncSession):
        """
        Initialize recommendation service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.engine = get_recommendation_engine()
    
    async def get_recommendations(
        self,
        user_id: str,
        top_k: int = 20,
        diversity: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> List[RecommendationResponse]:
        """
        Get personalized recommendations for user.
        
        Args:
            user_id: User ID
            top_k: Number of recommendations
            diversity: Diversity parameter (0-1)
            filters: Additional filters
            context: Context information
        
        Returns:
            List of recommendations
        """
        try:
            # Create recommendation request
            request = RecommendationRequest(
                user_id=user_id,
                top_k=top_k,
                context=context or {},
                filters=filters or {},
                diversity_lambda=diversity
            )
            
            # Get recommendations from engine
            recommendations = await self.engine.get_recommendations(request)
            
            # Convert to response schema
            return [
                RecommendationResponse(
                    movie_id=rec.movie_id,
                    score=rec.score,
                    components=rec.components,
                    explanation=rec.explanation,
                    confidence=rec.confidence,
                    metadata=rec.metadata
                )
                for rec in recommendations
            ]
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            raise MLModelError("RecommendationEngine", str(e))
    
    async def get_similar_movies(
        self,
        movie_id: int,
        top_k: int = 20,
        algorithm: str = "hybrid"
    ) -> List[Dict[str, Any]]:
        """
        Get movies similar to a specific movie.
        
        Args:
            movie_id: Target movie ID
            top_k: Number of similar movies
            algorithm: Algorithm to use (content, collaborative, hybrid)
        
        Returns:
            List of similar movies
        """
        try:
            if algorithm == "content":
                # Use content-based engine
                results = await self.engine.content_engine.get_similar_movies(
                    user_id=None,  # No user context needed
                    k=top_k,
                    filters={"movie_id": movie_id}
                )
            else:
                # Use hybrid approach
                results = await self.engine.content_engine.get_similar_movies(
                    user_id=None,
                    k=top_k,
                    filters={"movie_id": movie_id}
                )
            
            return results
            
        except Exception as e:
            logger.error(f"Similar movies retrieval failed: {e}")
            raise MLModelError("SimilarMovies", str(e))
    
    async def record_feedback(
        self,
        user_id: str,
        movie_id: int,
        feedback_type: str,
        accepted: bool,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Record user feedback on recommendation.
        
        Args:
            user_id: User ID
            movie_id: Movie ID
            feedback_type: Type of feedback
            accepted: Whether recommendation was accepted
            context: Additional context
        """
        # Store feedback for model retraining
        # This would typically write to a database or message queue
        
        logger.info(
            f"Recommendation feedback recorded: user={user_id}, "
            f"movie={movie_id}, type={feedback_type}, accepted={accepted}"
        )
