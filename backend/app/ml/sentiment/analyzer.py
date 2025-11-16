"""
Sentiment Analysis Engine using transformer models.
Analyzes movie reviews for sentiment and emotions.
"""

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, List, Any, Optional
import torch
import logging
import numpy as np

from app.core.config import settings
from app.core.exceptions import MLModelError
from app.core.logging import MLLogger

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Sentiment analysis using pre-trained transformer models.
    Supports sentiment classification and emotion detection.
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.sentiment_model = None
        self.emotion_model = None
        self.is_loaded = False
    
    def load_models(self):
        """Load sentiment and emotion models."""
        try:
            logger.info("Loading sentiment analysis models...")
            
            # Sentiment model (DistilBERT)
            self.sentiment_model = pipeline(
                "sentiment-analysis",
                model=settings.MODEL_BERT_PATH,
                device=0 if self.device == "cuda" else -1,
                max_length=settings.SENTIMENT_MAX_LENGTH,
                truncation=True
            )
            
            # Emotion detection model
            self.emotion_model = pipeline(
                "text-classification",
                model=settings.MODEL_EMOTION_PATH,
                device=0 if self.device == "cuda" else -1,
                top_k=None  # Return all emotion scores
            )
            
            self.is_loaded = True
            logger.info(f"Models loaded on {self.device}")
            
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            raise MLModelError("SentimentAnalyzer", f"Model loading failed: {e}")
    
    async def analyze_sentiment(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Analyze sentiment of text.
        
        Args:
            text: Text to analyze
        
        Returns:
            Sentiment analysis results {label, score, normalized_score}
        """
        if not self.is_loaded:
            self.load_models()
        
        try:
            # Run sentiment analysis
            result = self.sentiment_model(text)[0]
            
            # Normalize score to -1 (negative) to +1 (positive)
            label = result['label'].lower()
            confidence = result['score']
            
            if label == 'positive':
                normalized_score = confidence
            elif label == 'negative':
                normalized_score = -confidence
            else:  # neutral
                normalized_score = 0.0
            
            return {
                "label": label,
                "confidence": confidence,
                "sentiment_score": normalized_score
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {
                "label": "neutral",
                "confidence": 0.5,
                "sentiment_score": 0.0
            }
    
    async def detect_emotions(
        self,
        text: str
    ) -> Dict[str, float]:
        """
        Detect emotions in text.
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary of emotion scores
        """
        if not self.is_loaded:
            self.load_models()
        
        try:
            # Run emotion detection
            results = self.emotion_model(text)[0]
            
            # Convert to dictionary
            emotions = {}
            for result in results:
                emotion = result['label'].lower()
                score = result['score']
                emotions[emotion] = score
            
            return emotions
            
        except Exception as e:
            logger.error(f"Emotion detection failed: {e}")
            return {}
    
    async def analyze_review(
        self,
        review_text: str
    ) -> Dict[str, Any]:
        """
        Complete review analysis: sentiment + emotions.
        
        Args:
            review_text: Review text
        
        Returns:
            Complete analysis results
        """
        try:
            # Sentiment
            sentiment = await self.analyze_sentiment(review_text)
            
            # Emotions
            emotions = await self.detect_emotions(review_text)
            
            # Aspect-based sentiment (simplified)
            aspects = await self._analyze_aspects(review_text)
            
            return {
                "sentiment_score": sentiment["sentiment_score"],
                "sentiment_label": sentiment["label"],
                "sentiment_confidence": sentiment["confidence"],
                "emotions": emotions,
                "aspect_sentiments": aspects
            }
            
        except Exception as e:
            logger.error(f"Review analysis failed: {e}")
            return {
                "sentiment_score": 0.0,
                "sentiment_label": "neutral",
                "sentiment_confidence": 0.5,
                "emotions": {},
                "aspect_sentiments": {}
            }
    
    async def _analyze_aspects(
        self,
        review_text: str
    ) -> Dict[str, float]:
        """
        Analyze sentiment for specific aspects (plot, acting, etc.).
        Simplified implementation - checks for aspect keywords.
        """
        aspects = {
            "plot": ["plot", "story", "narrative", "storyline"],
            "acting": ["acting", "performance", "actor", "actress", "cast"],
            "cinematography": ["cinematography", "visual", "shot", "camera", "direction"],
            "soundtrack": ["soundtrack", "music", "score", "sound"]
        }
        
        aspect_sentiments = {}
        review_lower = review_text.lower()
        
        for aspect, keywords in aspects.items():
            # Check if aspect is mentioned
            if any(keyword in review_lower for keyword in keywords):
                # Extract sentences mentioning the aspect
                sentences = [s.strip() for s in review_text.split('.') if s.strip()]
                relevant_sentences = [
                    s for s in sentences 
                    if any(keyword in s.lower() for keyword in keywords)
                ]
                
                if relevant_sentences:
                    # Analyze sentiment of relevant sentences
                    combined_text = '. '.join(relevant_sentences)
                    sentiment = await self.analyze_sentiment(combined_text)
                    aspect_sentiments[aspect] = sentiment["sentiment_score"]
        
        return aspect_sentiments
    
    async def aggregate_movie_sentiment(
        self,
        reviews: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Aggregate sentiment across multiple reviews.
        
        Args:
            reviews: List of review dictionaries with sentiment scores
        
        Returns:
            Aggregated sentiment metrics
        """
        if not reviews:
            return {
                "average_sentiment": 0.0,
                "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0},
                "emotion_distribution": {},
                "review_count": 0
            }
        
        # Calculate average sentiment
        sentiment_scores = [r.get("sentiment_score", 0) for r in reviews]
        avg_sentiment = np.mean(sentiment_scores)
        
        # Sentiment distribution
        distribution = {
            "positive": sum(1 for s in sentiment_scores if s > 0.2),
            "neutral": sum(1 for s in sentiment_scores if -0.2 <= s <= 0.2),
            "negative": sum(1 for s in sentiment_scores if s < -0.2)
        }
        
        # Aggregate emotions
        emotion_counts = {}
        for review in reviews:
            emotions = review.get("emotions", {})
            for emotion, score in emotions.items():
                if emotion not in emotion_counts:
                    emotion_counts[emotion] = []
                emotion_counts[emotion].append(score)
        
        emotion_distribution = {
            emotion: np.mean(scores)
            for emotion, scores in emotion_counts.items()
        }
        
        return {
            "average_sentiment": avg_sentiment,
            "sentiment_distribution": distribution,
            "emotion_distribution": emotion_distribution,
            "review_count": len(reviews),
            "positive_ratio": distribution["positive"] / len(reviews) if reviews else 0
        }


# Singleton instance
_sentiment_analyzer = None


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Get singleton sentiment analyzer."""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentAnalyzer()
    return _sentiment_analyzer
