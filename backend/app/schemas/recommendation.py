"""
Recommendation Pydantic schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime


class RecommendationRequest(BaseModel):
    """Schema for recommendation request."""
    top_k: int = Field(20, ge=1, le=100, description="Number of recommendations")
    diversity: Optional[float] = Field(None, ge=0.0, le=1.0, description="Diversity parameter (0=relevance, 1=diversity)")
    mood: Optional[str] = Field(None, description="Current mood filter")
    genres: Optional[List[str]] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    exclude_watched: bool = True
    context: Optional[Dict[str, Any]] = None


class RecommendationResponse(BaseModel):
    """Schema for single recommendation."""
    movie_id: int
    score: float
    components: Dict[str, float]
    explanation: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = {}


class RecommendationsListResponse(BaseModel):
    """Schema for list of recommendations."""
    recommendations: List[RecommendationResponse]
    generated_at: str
    algorithm_version: str
    diversity_score: Optional[float] = None
    total_candidates: Optional[int] = None


class SimilarMoviesRequest(BaseModel):
    """Schema for similar movies request."""
    movie_id: int
    top_k: int = Field(20, ge=1, le=100)
    algorithm: Optional[str] = Field("hybrid", pattern=r'^(content|collaborative|hybrid)$')


class RecommendationFeedback(BaseModel):
    """Schema for recommendation feedback."""
    movie_id: int
    accepted: bool
    feedback_type: Optional[str] = Field(None, pattern=r'^(clicked|watched|rated|dismissed|disliked)$')
    context: Optional[Dict[str, Any]] = None


class ConversationalRecommendationRequest(BaseModel):
    """Schema for conversational recommendation request."""
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_history: Optional[List[Dict[str, str]]] = []


class ConversationalRecommendationResponse(BaseModel):
    """Schema for conversational recommendation response."""
    message: str
    recommended_movies: List[int] = []
    conversation_id: Optional[str] = None
