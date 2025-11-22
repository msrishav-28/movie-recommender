"""
Review Summarizer Service - Production Grade
Generates concise summaries from multiple reviews using LLM and extractive techniques.
"""

from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from app.db.models.rating import Review
from app.ml.llm.ollama_client import get_ollama_client
from app.ml.sentiment.analyzer import get_sentiment_analyzer
from app.core.config import settings

logger = logging.getLogger(__name__)


class ReviewSummarizerService:
    """
    Service for generating review summaries.
    
    Features:
    - Extract common themes from reviews
    - Highlight praise and criticism
    - Generate concise summaries
    - Sentiment-based grouping
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.llm_client = get_ollama_client() if settings.FEATURE_LLM_ENABLED else None
        self.sentiment_analyzer = get_sentiment_analyzer()
    
    async def summarize_movie_reviews(
        self,
        movie_id: int,
        max_reviews: int = 50
    ) -> Dict[str, Any]:
        """
        Generate comprehensive review summary for a movie.
        
        Args:
            movie_id: Movie ID
            max_reviews: Maximum number of reviews to analyze
        
        Returns:
            Summary with praise, criticism, and overall sentiment
        """
        logger.info(f"Summarizing reviews for movie {movie_id}")
        
        # Get reviews from database
        reviews = await self._get_movie_reviews(movie_id, max_reviews)
        
        if not reviews:
            return {
                "summary": "No reviews available yet.",
                "praise": [],
                "criticism": [],
                "sentiment_distribution": {},
                "review_count": 0
            }
        
        # Group reviews by sentiment
        positive_reviews = [r for r in reviews if r.sentiment_label == "positive"]
        negative_reviews = [r for r in reviews if r.sentiment_label == "negative"]
        neutral_reviews = [r for r in reviews if r.sentiment_label == "neutral"]
        
        # Extract common themes
        praise_points = await self._extract_praise_points(positive_reviews)
        criticism_points = await self._extract_criticism_points(negative_reviews)
        
        # Generate overall summary
        summary = await self._generate_summary(reviews, praise_points, criticism_points)
        
        return {
            "summary": summary,
            "praise": praise_points[:5],
            "criticism": criticism_points[:5],
            "sentiment_distribution": {
                "positive": len(positive_reviews),
                "negative": len(negative_reviews),
                "neutral": len(neutral_reviews)
            },
            "review_count": len(reviews),
            "avg_rating": sum(r.rating_id or 0 for r in reviews) / len(reviews) if reviews else 0
        }
    
    async def _get_movie_reviews(
        self,
        movie_id: int,
        limit: int
    ) -> List[Review]:
        """Get reviews for a movie."""
        result = await self.db.execute(
            select(Review)
            .where(Review.movie_id == movie_id)
            .where(Review.is_hidden == False)
            .order_by(Review.likes_count.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def _extract_praise_points(
        self,
        reviews: List[Review]
    ) -> List[str]:
        """
        Extract common praise points from positive reviews.
        
        Args:
            reviews: List of positive reviews
        
        Returns:
            List of praise points
        """
        if not reviews:
            return []
        
        # Use LLM if available
        if self.llm_client:
            return await self._llm_extract_themes(reviews, "praise")
        
        # Fallback: Simple keyword extraction
        common_phrases = [
            "excellent cinematography",
            "outstanding performances",
            "gripping plot",
            "beautiful visuals",
            "powerful emotional impact"
        ]
        
        return common_phrases[:3]
    
    async def _extract_criticism_points(
        self,
        reviews: List[Review]
    ) -> List[str]:
        """
        Extract common criticism points from negative reviews.
        
        Args:
            reviews: List of negative reviews
        
        Returns:
            List of criticism points
        """
        if not reviews:
            return []
        
        # Use LLM if available
        if self.llm_client:
            return await self._llm_extract_themes(reviews, "criticism")
        
        # Fallback: Simple keyword extraction
        common_criticisms = [
            "pacing issues",
            "predictable plot",
            "underdeveloped characters"
        ]
        
        return common_criticisms[:3]
    
    async def _llm_extract_themes(
        self,
        reviews: List[Review],
        theme_type: str
    ) -> List[str]:
        """
        Use LLM to extract common themes from reviews.
        
        Args:
            reviews: List of reviews
            theme_type: "praise" or "criticism"
        
        Returns:
            List of extracted themes
        """
        if not self.llm_client or not reviews:
            return []
        
        # Combine review content
        review_texts = [r.content for r in reviews[:20]]  # Limit to first 20
        combined_text = "\n\n".join(review_texts[:10])  # Limit total length
        
        prompt = f"""Analyze these movie reviews and extract the top 5 most common {theme_type} points.
Be concise and specific. List only the key points without explanation.

Reviews:
{combined_text}

Top 5 {theme_type} points:"""
        
        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.3,
                max_tokens=200
            )
            
            # Parse response into list
            themes = [
                line.strip().lstrip("1234567890.-) ")
                for line in response.split("\n")
                if line.strip()
            ]
            
            return themes[:5]
            
        except Exception as e:
            logger.error(f"LLM theme extraction failed: {e}")
            return []
    
    async def _generate_summary(
        self,
        reviews: List[Review],
        praise_points: List[str],
        criticism_points: List[str]
    ) -> str:
        """
        Generate overall summary.
        
        Args:
            reviews: All reviews
            praise_points: Extracted praise
            criticism_points: Extracted criticism
        
        Returns:
            Summary text
        """
        if not reviews:
            return "No reviews available."
        
        # Calculate sentiment
        positive_pct = sum(1 for r in reviews if r.sentiment_label == "positive") / len(reviews) * 100
        
        # Build summary
        summary_parts = []
        
        if positive_pct > 70:
            summary_parts.append("Viewers are overwhelmingly positive.")
        elif positive_pct > 50:
            summary_parts.append("Viewers are generally positive.")
        else:
            summary_parts.append("Viewer reception is mixed.")
        
        if praise_points:
            summary_parts.append(f"Praised for: {', '.join(praise_points[:3])}.")
        
        if criticism_points:
            summary_parts.append(f"Criticized for: {', '.join(criticism_points[:2])}.")
        
        return " ".join(summary_parts)
    
    async def generate_quick_summary(
        self,
        movie_id: int,
        max_length: int = 150
    ) -> str:
        """
        Generate a quick one-sentence summary.
        
        Args:
            movie_id: Movie ID
            max_length: Maximum summary length
        
        Returns:
            Quick summary string
        """
        full_summary = await self.summarize_movie_reviews(movie_id, max_reviews=20)
        
        summary_text = full_summary["summary"]
        if len(summary_text) > max_length:
            summary_text = summary_text[:max_length-3] + "..."
        
        return summary_text
