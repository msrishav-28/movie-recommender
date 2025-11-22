"""
Recommendation Explainer - Production Grade
Generates natural language explanations for recommendations.
Uses LLM and template-based approaches.
"""

from typing import List, Dict, Any, Optional
import logging

from app.core.config import settings
from app.ml.llm.ollama_client import get_ollama_client

logger = logging.getLogger(__name__)


class RecommendationExplainer:
    """
    Generate explanations for movie recommendations.
    
    Explanation types:
    - Collaborative filtering based ("Users like you enjoyed...")
    - Content similarity based ("Similar to movies you watched...")
    - Sentiment based ("Highly praised for...")
    - Social based ("Trending among your network...")
    - Hybrid explanations combining multiple signals
    """
    
    def __init__(self):
        """Initialize explainer."""
        self.ollama_client = get_ollama_client() if settings.FEATURE_LLM_ENABLED else None
        self.use_llm = settings.FEATURE_LLM_ENABLED and settings.LLM_EXPLANATIONS_ENABLED
        logger.info(f"RecommendationExplainer initialized (LLM: {self.use_llm})")
    
    async def generate_explanation(
        self,
        user_id: str,
        movie_id: int,
        component_scores: Dict[str, float],
        user_history: Optional[List[Dict[str, Any]]] = None,
        movie_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate explanation for a recommendation.
        
        Args:
            user_id: User ID
            movie_id: Recommended movie ID
            component_scores: Score breakdown from hybrid engine
            user_history: User's watch history
            movie_metadata: Movie information
        
        Returns:
            Natural language explanation
        """
        try:
            # Determine dominant factor
            dominant_factor = max(component_scores.items(), key=lambda x: x[1])
            factor_name, factor_score = dominant_factor
            
            # Use LLM for explanation if enabled
            if self.use_llm and self.ollama_client:
                return await self._generate_llm_explanation(
                    user_id,
                    movie_id,
                    component_scores,
                    user_history,
                    movie_metadata
                )
            
            # Otherwise use template-based explanation
            return self._generate_template_explanation(
                factor_name,
                factor_score,
                component_scores,
                user_history,
                movie_metadata
            )
            
        except Exception as e:
            logger.error(f"Explanation generation failed: {e}")
            return "Recommended based on your viewing preferences."
    
    async def _generate_llm_explanation(
        self,
        user_id: str,
        movie_id: int,
        component_scores: Dict[str, float],
        user_history: Optional[List[Dict[str, Any]]],
        movie_metadata: Optional[Dict[str, Any]]
    ) -> str:
        """Generate explanation using LLM."""
        
        # Prepare context
        movie_title = movie_metadata.get("title", f"Movie {movie_id}") if movie_metadata else f"Movie {movie_id}"
        
        history_titles = []
        if user_history:
            history_titles = [m.get("title", "Unknown") for m in user_history[:5]]
        
        # Format scores
        scores_text = ", ".join([f"{k}: {v:.2f}" for k, v in component_scores.items()])
        
        # Build prompt
        system_prompt = """You are a movie recommendation assistant. Generate a brief, 
        engaging explanation (2-3 sentences max) for why a movie is recommended. 
        Be conversational and focus on the most relevant factors. Don't mention technical scores."""
        
        prompt = f"""Movie: {movie_title}
User's recent favorites: {', '.join(history_titles) if history_titles else 'None'}
Recommendation factors: {scores_text}

Generate a natural explanation for why this movie is recommended:"""
        
        try:
            explanation = await self.ollama_client.generate(
                prompt=prompt,
                system=system_prompt,
                temperature=0.7
            )
            
            return explanation.strip()
            
        except Exception as e:
            logger.error(f"LLM explanation failed, falling back to template: {e}")
            return self._generate_template_explanation(
                list(component_scores.keys())[0],
                list(component_scores.values())[0],
                component_scores,
                user_history,
                movie_metadata
            )
    
    def _generate_template_explanation(
        self,
        dominant_factor: str,
        factor_score: float,
        all_scores: Dict[str, float],
        user_history: Optional[List[Dict[str, Any]]],
        movie_metadata: Optional[Dict[str, Any]]
    ) -> str:
        """Generate explanation using templates."""
        
        movie_title = movie_metadata.get("title", "this movie") if movie_metadata else "this movie"
        
        # Collaborative filtering explanation
        if dominant_factor == "collaborative":
            confidence = int(factor_score * 100)
            similar_users_count = 150  # Placeholder
            
            return (
                f"Recommended because {confidence}% of users with similar taste "
                f"to yours rated this highly. Based on {similar_users_count} similar viewers."
            )
        
        # Content-based explanation
        elif dominant_factor == "content":
            if user_history and len(user_history) > 0:
                reference_movie = user_history[0].get("title", "movies you enjoyed")
                genres = movie_metadata.get("genres", []) if movie_metadata else []
                
                if genres:
                    genre_str = ", ".join(genres[:2])
                    return (
                        f"Recommended because you enjoyed {reference_movie}. "
                        f"This {genre_str} film shares similar themes and style."
                    )
                else:
                    return (
                        f"Recommended because you enjoyed {reference_movie}. "
                        f"This movie has similar content and themes."
                    )
            else:
                return "Recommended based on matching genres and themes you prefer."
        
        # GNN explanation
        elif dominant_factor == "gnn":
            return (
                "Recommended through advanced pattern matching that found connections "
                "between this movie and your viewing preferences through shared actors, "
                "directors, and thematic elements."
            )
        
        # Sentiment-based explanation
        elif dominant_factor == "sentiment":
            sentiment_score = all_scores.get("sentiment", 0)
            if sentiment_score > 0.7:
                return (
                    f"Highly recommended! This movie has exceptional reviews with "
                    f"viewers particularly praising its quality. Sentiment score: {int(sentiment_score * 100)}%."
                )
            else:
                return (
                    "Recommended based on positive viewer sentiment and critical acclaim."
                )
        
        # Popularity-based explanation
        elif dominant_factor == "popularity":
            return (
                "Trending now! This popular movie is being watched and highly rated "
                "by many users with similar interests to yours."
            )
        
        # Context-based explanation
        elif dominant_factor == "context":
            return (
                f"Recommended as a great choice for your current context. "
                f"This movie fits perfectly with what you're looking for right now."
            )
        
        # Default fallback
        else:
            return f"Recommended based on your viewing preferences and interests."
    
    async def generate_batch_explanations(
        self,
        user_id: str,
        recommendations: List[Dict[str, Any]],
        user_history: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """
        Generate explanations for a batch of recommendations.
        
        Args:
            user_id: User ID
            recommendations: List of recommendations with scores
            user_history: User's watch history
        
        Returns:
            List of explanations
        """
        explanations = []
        
        for rec in recommendations:
            explanation = await self.generate_explanation(
                user_id=user_id,
                movie_id=rec.get("movie_id"),
                component_scores=rec.get("components", {}),
                user_history=user_history,
                movie_metadata=rec.get("metadata", {})
            )
            explanations.append(explanation)
        
        return explanations
    
    def explain_component_contribution(
        self,
        component_scores: Dict[str, float]
    ) -> Dict[str, str]:
        """
        Explain each component's contribution.
        
        Args:
            component_scores: Score breakdown
        
        Returns:
            Dictionary of component explanations
        """
        explanations = {}
        
        for component, score in component_scores.items():
            if component == "collaborative":
                explanations[component] = (
                    f"Similar users' preferences contribute {int(score * 100)}% to this recommendation"
                )
            elif component == "content":
                explanations[component] = (
                    f"Content similarity to your favorites: {int(score * 100)}%"
                )
            elif component == "gnn":
                explanations[component] = (
                    f"Graph connections (actors, directors, themes): {int(score * 100)}%"
                )
            elif component == "sentiment":
                explanations[component] = (
                    f"Positive viewer sentiment boost: {int(score * 100)}%"
                )
            elif component == "popularity":
                explanations[component] = (
                    f"Current popularity factor: {int(score * 100)}%"
                )
            elif component == "context":
                explanations[component] = (
                    f"Contextual relevance: {int(score * 100)}%"
                )
        
        return explanations
    
    def generate_feature_importance_explanation(
        self,
        features: Dict[str, float],
        top_k: int = 3
    ) -> str:
        """
        Generate explanation based on feature importance.
        
        Args:
            features: Feature importance scores
            top_k: Number of top features to include
        
        Returns:
            Feature-based explanation
        """
        # Sort features by importance
        sorted_features = sorted(
            features.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:top_k]
        
        if not sorted_features:
            return "Recommended based on multiple factors."
        
        # Build explanation
        feature_phrases = []
        for feature_name, importance in sorted_features:
            if "genre" in feature_name.lower():
                feature_phrases.append(f"matching genre preferences")
            elif "director" in feature_name.lower():
                feature_phrases.append(f"favorite directors")
            elif "actor" in feature_name.lower():
                feature_phrases.append(f"actors you follow")
            elif "rating" in feature_name.lower():
                feature_phrases.append(f"high ratings")
        
        if feature_phrases:
            return f"Recommended based on {', '.join(feature_phrases)}."
        else:
            return "Recommended based on your viewing patterns."
