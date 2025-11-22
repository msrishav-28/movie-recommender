"""Recommendation endpoints."""

from fastapi import APIRouter, Depends, Query
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.api.deps import get_current_active_user, get_db
from app.db.models.user import User
from app.schemas.recommendation import (
    RecommendationResponse,
    RecommendationsListResponse,
    RecommendationFeedback
)
from app.services.recommendation_service import RecommendationService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=RecommendationsListResponse)
async def get_recommendations(
    top_k: int = Query(20, ge=1, le=100),
    diversity: Optional[float] = Query(None, ge=0.0, le=1.0),
    mood: Optional[str] = Query(None),
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized movie recommendations for current user.
    
    - **top_k**: Number of recommendations (default: 20)
    - **diversity**: Diversity parameter 0-1 (default: 0.7)
    - **mood**: Optional mood filter
    """
    service = RecommendationService(db)
    
    context = {}
    if mood:
        context["mood"] = mood
    
    recommendations = await service.get_recommendations(
        user_id=str(user.id),
        top_k=top_k,
        diversity=diversity,
        context=context
    )
    
    return RecommendationsListResponse(
        recommendations=recommendations,
        generated_at=datetime.utcnow().isoformat() + "Z",
        algorithm_version="hybrid-v1.0"
    )


@router.get("/similar/{movie_id}", response_model=List[RecommendationResponse])
async def get_similar_movies(
    movie_id: int,
    top_k: int = Query(20, ge=1, le=100),
    algorithm: str = Query("hybrid", pattern=r'^(content|collaborative|hybrid)$'),
    db: AsyncSession = Depends(get_db)
):
    """
    Get movies similar to a specific movie.
    
    - **movie_id**: Target movie ID
    - **top_k**: Number of similar movies
    - **algorithm**: Algorithm to use (content, collaborative, hybrid)
    """
    service = RecommendationService(db)
    
    similar = await service.get_similar_movies(
        movie_id=movie_id,
        top_k=top_k,
        algorithm=algorithm
    )
    
    return [
        RecommendationResponse(
            movie_id=item["movie_id"],
            score=item["score"],
            components=item.get("components", {}),
            explanation=item.get("explanation", "Similar movie"),
            confidence=item.get("confidence", 0.8),
            metadata=item.get("metadata", {})
        )
        for item in similar
    ]


@router.post("/feedback")
async def record_recommendation_feedback(
    feedback: RecommendationFeedback,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Record user feedback on a recommendation.
    
    - **movie_id**: Recommended movie ID
    - **accepted**: Whether user accepted the recommendation
    - **feedback_type**: Type of feedback (clicked, watched, rated, dismissed, disliked)
    """
    service = RecommendationService(db)
    
    await service.record_feedback(
        user_id=str(user.id),
        movie_id=feedback.movie_id,
        feedback_type=feedback.feedback_type or "clicked",
        accepted=feedback.accepted,
        context=feedback.context
    )
    
    return {"status": "recorded", "message": "Feedback recorded successfully"}


@router.post("/aesthetic", response_model=List[RecommendationResponse])
async def get_aesthetic_recommendations(
    query: str,
    limit: int = Query(24, ge=1, le=100),
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get recommendations based on aesthetic/vibe query.
    
    - **query**: Natural language aesthetic description
    - **limit**: Number of recommendations
    """
    service = RecommendationService(db)
    
    # Placeholder implementation
    recommendations = await service.get_recommendations(
        user_id=str(user.id),
        top_k=limit,
        diversity=0.7,
        context={"aesthetic_query": query}
    )
    
    return recommendations


@router.post("/cold-start", response_model=List[RecommendationResponse])
async def get_cold_start_recommendations(
    preferences: dict,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get recommendations for users with no history (cold start).
    
    - **preferences**: User's genre/mood preferences
    """
    service = RecommendationService(db)
    
    recommendations = await service.get_recommendations(
        user_id=str(user.id),
        top_k=preferences.get("limit", 20),
        diversity=0.5,
        context={"preferences": preferences, "cold_start": True}
    )
    
    return recommendations


@router.get("/explain/{movie_id}")
async def explain_recommendation(
    movie_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get explanation for why a movie was recommended.
    
    - **movie_id**: Movie ID to explain
    """
    
    # Placeholder implementation
    return {
        "explanation": f"This movie was recommended based on your viewing history and preferences.",
        "reasons": [
            "Matches your preferred genre",
            "Similar to movies you've rated highly",
            "Popular among users with similar tastes",
            "High critical acclaim"
        ]
    }
