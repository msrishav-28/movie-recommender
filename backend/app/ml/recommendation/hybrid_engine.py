"""
Hybrid Recommendation Engine - Production Grade
Combines collaborative filtering, content-based, GNN, and sentiment analysis.
Implements two-stage retrieval and ranking with diversity optimization.
"""

from typing import List, Dict, Any, Optional
import asyncio
import time
import numpy as np
from collections import defaultdict
import logging

from app.core.config import settings
from app.core.exceptions import MLModelError, ResourceNotFoundError
from app.core.logging import MLLogger
from app.cache.cache_manager import CacheManager
from app.ml.recommendation.collaborative import CollaborativeFilteringEngine
from app.ml.recommendation.content_based import ContentBasedEngine
from app.ml.recommendation.gnn_recommender import GNNRecommender
from app.ml.recommendation.diversity import DiversityOptimizer
from app.ml.recommendation.explainer import RecommendationExplainer

logger = logging.getLogger(__name__)


class RecommendationRequest:
    """Request parameters for recommendations."""
    
    def __init__(
        self,
        user_id: str,
        top_k: int = 20,
        context: Optional[Dict[str, Any]] = None,
        filters: Optional[Dict[str, Any]] = None,
        diversity_lambda: Optional[float] = None
    ):
        self.user_id = user_id
        self.top_k = top_k
        self.context = context or {}
        self.filters = filters or {}
        self.diversity_lambda = diversity_lambda or settings.REC_DIVERSITY_LAMBDA


class Recommendation:
    """Single recommendation result."""
    
    def __init__(
        self,
        movie_id: int,
        score: float,
        components: Dict[str, float],
        explanation: str,
        confidence: float,
        metadata: Dict[str, Any]
    ):
        self.movie_id = movie_id
        self.score = score
        self.components = components
        self.explanation = explanation
        self.confidence = confidence
        self.metadata = metadata
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "movie_id": self.movie_id,
            "score": round(self.score, 4),
            "components": {k: round(v, 4) for k, v in self.components.items()},
            "explanation": self.explanation,
            "confidence": round(self.confidence, 4),
            "metadata": self.metadata
        }


class HybridRecommendationEngine:
    """
    Main hybrid recommendation engine.
    
    Architecture:
    1. Candidate Generation (fetch 200 candidates from multiple sources)
    2. Re-ranking (score each candidate with hybrid model)
    3. Diversification (MMR to prevent filter bubbles)
    4. Explanation Generation (LLM-based explanations)
    """
    
    def __init__(self):
        """Initialize all sub-engines and components."""
        self.collaborative_engine = CollaborativeFilteringEngine()
        self.content_engine = ContentBasedEngine()
        self.gnn_engine = GNNRecommender() if settings.FEATURE_GNN_ENABLED else None
        self.diversity_optimizer = DiversityOptimizer()
        self.explainer = RecommendationExplainer()
        self.cache_manager = CacheManager()
        
        # Component weights from settings
        self.weights = {
            "collaborative": settings.REC_COLLABORATIVE_WEIGHT,
            "content": settings.REC_CONTENT_WEIGHT,
            "gnn": settings.REC_GNN_WEIGHT,
            "sentiment": settings.REC_SENTIMENT_WEIGHT,
            "popularity": settings.REC_POPULARITY_WEIGHT,
            "context": settings.REC_CONTEXT_WEIGHT
        }
        
        logger.info("HybridRecommendationEngine initialized with weights: %s", self.weights)
    
    async def get_recommendations(
        self,
        request: RecommendationRequest
    ) -> List[Recommendation]:
        """
        Generate recommendations for a user.
        
        Args:
            request: RecommendationRequest with user_id and parameters
        
        Returns:
            List of Recommendation objects
        """
        start_time = time.time()
        
        try:
            # Check cache first
            cache_key = self._get_cache_key(request)
            cached = await self.cache_manager.get(cache_key)
            if cached:
                logger.info(f"Returning cached recommendations for user {request.user_id}")
                return [Recommendation(**r) for r in cached]
            
            # Stage 1: Candidate Generation
            logger.info(f"Generating candidates for user {request.user_id}")
            candidates = await self._generate_candidates(
                request.user_id,
                k=settings.REC_CANDIDATE_POOL_SIZE,
                filters=request.filters
            )
            
            if not candidates:
                raise ResourceNotFoundError("candidates", f"user_{request.user_id}")
            
            # Stage 2: Re-ranking
            logger.info(f"Re-ranking {len(candidates)} candidates")
            scored_candidates = await self._rank_candidates(
                user_id=request.user_id,
                candidates=candidates,
                context=request.context
            )
            
            # Stage 3: Diversification
            logger.info("Applying diversity optimization")
            diverse_candidates = await self.diversity_optimizer.apply_mmr(
                candidates=scored_candidates,
                lambda_param=request.diversity_lambda,
                top_k=request.top_k
            )
            
            # Stage 4: Explanation Generation
            logger.info("Generating explanations")
            recommendations = await self._generate_explanations(
                user_id=request.user_id,
                candidates=diverse_candidates
            )
            
            # Cache results
            await self.cache_manager.set(
                cache_key,
                [r.to_dict() for r in recommendations],
                ttl=settings.REC_CACHE_TTL
            )
            
            # Log metrics
            duration_ms = (time.time() - start_time) * 1000
            MLLogger.log_prediction(
                model_name="HybridRecommendationEngine",
                user_id=request.user_id,
                duration_ms=duration_ms,
                num_results=len(recommendations)
            )
            
            logger.info(
                f"Generated {len(recommendations)} recommendations for user {request.user_id} "
                f"in {duration_ms:.2f}ms"
            )
            
            return recommendations
            
        except Exception as e:
            MLLogger.log_model_error("HybridRecommendationEngine", e)
            raise MLModelError("HybridRecommendationEngine", str(e))
    
    async def _generate_candidates(
        self,
        user_id: str,
        k: int,
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Stage 1: Generate candidate movies from multiple sources.
        
        Distribution:
        - 40% from collaborative filtering
        - 30% from content-based
        - 20% from GNN (if enabled)
        - 10% from trending/popular
        """
        tasks = []
        
        # Collaborative filtering candidates (40%)
        tasks.append(self.collaborative_engine.get_similar_users_movies(
            user_id=user_id,
            k=int(k * 0.4),
            filters=filters
        ))
        
        # Content-based candidates (30%)
        tasks.append(self.content_engine.get_similar_movies(
            user_id=user_id,
            k=int(k * 0.3),
            filters=filters
        ))
        
        # GNN candidates (20%) if enabled
        if self.gnn_engine:
            tasks.append(self.gnn_engine.get_graph_recommendations(
                user_id=user_id,
                k=int(k * 0.2),
                filters=filters
            ))
        
        # Trending/Popular candidates (10%)
        tasks.append(self._get_trending_movies(
            k=int(k * 0.1),
            filters=filters
        ))
        
        # Execute all candidate generation in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Merge and deduplicate candidates
        all_candidates = []
        seen_movie_ids = set()
        
        for result in results:
            if isinstance(result, Exception):
                logger.warning(f"Candidate generation error: {result}")
                continue
            
            for candidate in result:
                movie_id = candidate.get("movie_id")
                if movie_id not in seen_movie_ids:
                    seen_movie_ids.add(movie_id)
                    all_candidates.append(candidate)
        
        logger.info(f"Generated {len(all_candidates)} unique candidates from {len(tasks)} sources")
        return all_candidates
    
    async def _rank_candidates(
        self,
        user_id: str,
        candidates: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Stage 2: Re-rank candidates with hybrid scoring.
        
        Score = weighted sum of:
        - Collaborative filtering score (35%)
        - Content similarity score (25%)
        - GNN score (20%)
        - Sentiment boost (10%)
        - Popularity score (5%)
        - Context adjustment (5%)
        """
        scored_candidates = []
        
        # Get user profile for content matching
        user_profile = await self._get_user_profile(user_id)
        
        for candidate in candidates:
            movie_id = candidate.get("movie_id")
            
            try:
                # Calculate component scores
                scores = await self._calculate_component_scores(
                    user_id=user_id,
                    movie_id=movie_id,
                    candidate=candidate,
                    user_profile=user_profile,
                    context=context
                )
                
                # Weighted sum
                final_score = sum(
                    self.weights[component] * score
                    for component, score in scores.items()
                )
                
                # Add to results
                scored_candidates.append({
                    "movie_id": movie_id,
                    "score": final_score,
                    "components": scores,
                    "metadata": candidate.get("metadata", {})
                })
                
            except Exception as e:
                logger.warning(f"Error scoring candidate {movie_id}: {e}")
                continue
        
        # Sort by score
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)
        
        logger.info(f"Ranked {len(scored_candidates)} candidates")
        return scored_candidates
    
    async def _calculate_component_scores(
        self,
        user_id: str,
        movie_id: int,
        candidate: Dict[str, Any],
        user_profile: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate all component scores for a movie."""
        
        # Collaborative filtering score
        collab_score = await self.collaborative_engine.predict_rating(user_id, movie_id)
        
        # Content similarity score
        content_score = await self.content_engine.calculate_similarity(
            user_profile, 
            candidate
        )
        
        # GNN score
        if self.gnn_engine:
            gnn_score = await self.gnn_engine.predict_score(user_id, movie_id)
        else:
            gnn_score = 0.0
        
        # Sentiment boost
        sentiment_score = candidate.get("sentiment_score", 0.0)
        
        # Popularity score (normalized 0-1)
        popularity = candidate.get("popularity", 0.0)
        popularity_score = min(popularity / 100.0, 1.0)
        
        # Context adjustment (time of day, device, etc.)
        context_score = self._calculate_context_score(candidate, context)
        
        return {
            "collaborative": collab_score,
            "content": content_score,
            "gnn": gnn_score,
            "sentiment": sentiment_score,
            "popularity": popularity_score,
            "context": context_score
        }
    
    def _calculate_context_score(
        self,
        candidate: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """
        Adjust score based on context (time, device, mood, etc.).
        """
        score = 0.5  # Base score
        
        # Time of day adjustment
        hour = context.get("hour")
        if hour is not None:
            runtime = candidate.get("runtime", 120)
            # Prefer shorter movies late at night
            if hour >= 22 and runtime < 100:
                score += 0.2
            # Prefer longer movies on weekends
            if context.get("is_weekend") and runtime > 140:
                score += 0.1
        
        # Mood matching
        user_mood = context.get("mood")
        if user_mood:
            movie_moods = candidate.get("moods", [])
            if user_mood in movie_moods:
                score += 0.3
        
        # Device optimization
        device = context.get("device")
        if device == "mobile":
            # Prefer visually stunning movies for mobile viewing
            if candidate.get("cinematography_rating", 0) > 4.0:
                score += 0.1
        
        return min(score, 1.0)
    
    async def _generate_explanations(
        self,
        user_id: str,
        candidates: List[Dict[str, Any]]
    ) -> List[Recommendation]:
        """
        Stage 4: Generate natural language explanations.
        """
        recommendations = []
        
        # Get user history for explanation context
        user_history = await self._get_user_history(user_id, limit=10)
        
        for candidate in candidates:
            # Generate explanation
            explanation = await self.explainer.generate_explanation(
                user_id=user_id,
                movie_id=candidate["movie_id"],
                component_scores=candidate["components"],
                user_history=user_history
            )
            
            # Calculate confidence based on score variance
            confidence = self._calculate_confidence(candidate["components"])
            
            recommendations.append(Recommendation(
                movie_id=candidate["movie_id"],
                score=candidate["score"],
                components=candidate["components"],
                explanation=explanation,
                confidence=confidence,
                metadata=candidate["metadata"]
            ))
        
        return recommendations
    
    def _calculate_confidence(self, components: Dict[str, float]) -> float:
        """
        Calculate recommendation confidence based on component score agreement.
        Higher when multiple components agree, lower when they disagree.
        """
        scores = list(components.values())
        if not scores:
            return 0.5
        
        # Calculate coefficient of variation
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        
        if mean_score == 0:
            return 0.5
        
        cv = std_score / mean_score
        
        # Convert to confidence (lower CV = higher confidence)
        confidence = 1.0 / (1.0 + cv)
        
        return confidence
    
    async def _get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user taste profile."""
        # This would query the database for user preferences, ratings, etc.
        # Placeholder implementation
        return {
            "user_id": user_id,
            "favorite_genres": [],
            "favorite_actors": [],
            "favorite_directors": [],
            "average_rating": 3.5
        }
    
    async def _get_user_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user watch history and ratings."""
        # Placeholder - would query database
        return []
    
    async def _get_trending_movies(
        self,
        k: int,
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Get currently trending movies."""
        # Placeholder - would query trending from cache/database
        return []
    
    def _get_cache_key(self, request: RecommendationRequest) -> str:
        """Generate cache key for request."""
        return f"recommendations:{request.user_id}:{request.top_k}:{hash(str(request.filters))}"


# Singleton instance
_engine_instance = None

def get_recommendation_engine() -> HybridRecommendationEngine:
    """Get singleton recommendation engine instance."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = HybridRecommendationEngine()
    return _engine_instance
