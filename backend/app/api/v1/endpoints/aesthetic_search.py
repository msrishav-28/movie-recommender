"""
Aesthetic/Semantic Search endpoints.
World's first "rain with pink skies" style movie search.
"""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from app.api.deps import get_optional_user
from app.db.models.user import User

router = APIRouter()


class AestheticSearchResult(BaseModel):
    movie_id: int
    score: float
    num_matching_frames: int
    best_frames: List[Dict[str, Any]]
    visual_summary: Dict[str, Any]


class AestheticSearchResponse(BaseModel):
    results: List[AestheticSearchResult]
    query: str
    processing_time_ms: float


@router.get("/", response_model=AestheticSearchResponse)
async def search_by_aesthetic(
    query: str = Query(..., min_length=3, description="Aesthetic description"),
    top_k: int = Query(20, ge=1, le=100),
    min_score: Optional[float] = Query(None, ge=0.0, le=1.0),
    user: Optional[User] = Depends(get_optional_user)
):
    """
    🌟 **World's First Semantic Aesthetic Search**
    
    Search movies by visual aesthetics, mood, and atmosphere using natural language.
    
    **Example queries:**
    - "rain with pink skies and neon lights"
    - "warm autumn colors in countryside"
    - "melancholic urban scenes at night"
    - "symmetrical compositions with pastel colors"
    - "golden hour beach scenes with romantic feeling"
    
    - **query**: Natural language description of desired aesthetic
    - **top_k**: Number of results (default: 20)
    - **min_score**: Minimum similarity score 0-1 (default: 0.3)
    """
    import time
    from app.ml.semantic_search.clip_engine import get_aesthetic_search_engine
    
    start_time = time.time()
    
    engine = get_aesthetic_search_engine()
    search_results = await engine.search_by_aesthetic(
        query=query,
        filters=None,
        top_k=top_k,
        min_score=min_score
    )
    
    results = [
        AestheticSearchResult(
            movie_id=result.movie_id,
            score=result.score,
            num_matching_frames=len(result.matching_frames),
            best_frames=[
                {
                    "frame_number": frame.frame_number,
                    "timestamp": frame.timestamp,
                    "score": frame.score,
                    "frame_path": frame.frame_path
                }
                for frame in result.matching_frames[:3]
            ],
            visual_summary=result.visual_summary
        )
        for result in search_results
    ]
    
    processing_time = (time.time() - start_time) * 1000
    
    return AestheticSearchResponse(
        results=results,
        query=query,
        processing_time_ms=processing_time
    )


@router.post("/by-color")
async def search_by_color_palette(
    colors: List[str] = Query(..., description="Hex color codes"),
    tolerance: float = Query(0.1, ge=0.0, le=1.0),
    top_k: int = Query(20, ge=1, le=100)
):
    """
    Search movies by specific color palette.
    
    - **colors**: List of hex color codes (e.g., ["#FF5733", "#C70039"])
    - **tolerance**: Color matching tolerance 0-1
    - **top_k**: Number of results
    """
    from app.ml.semantic_search.clip_engine import get_aesthetic_search_engine
    
    engine = get_aesthetic_search_engine()
    results = await engine.search_by_color_palette(
        colors=colors,
        tolerance=tolerance,
        top_k=top_k
    )
    
    return {
        "results": [result.to_dict() for result in results],
        "colors": colors
    }


@router.post("/by-image")
async def search_by_reference_image(
    image_url: str,
    top_k: int = Query(20, ge=1, le=100)
):
    """
    Search movies visually similar to a reference image.
    
    - **image_url**: URL of reference image
    - **top_k**: Number of results
    """
    
    from app.ml.semantic_search.clip_engine import get_aesthetic_search_engine
    
    engine = get_aesthetic_search_engine()
    results = await engine.search_by_reference_image(
        image_path=image_url,
        top_k=top_k
    )
    
    return {
        "results": [result.to_dict() for result in results],
        "image_url": image_url
    }


@router.get("/examples")
async def get_example_queries():
    """
    Get example aesthetic search queries to inspire users.
    """
    
    return {
        "examples": [
            {
                "category": "Weather & Atmosphere",
                "queries": [
                    "rain with neon reflections and loneliness",
                    "snowy landscapes with isolation",
                    "foggy morning scenes with mystery",
                    "thunderstorm with dramatic lighting"
                ]
            },
            {
                "category": "Colors & Lighting",
                "queries": [
                    "pink and purple sunset skies",
                    "warm golden hour lighting",
                    "cold blue isolated atmosphere",
                    "vibrant neon cyberpunk colors"
                ]
            },
            {
                "category": "Mood & Emotion",
                "queries": [
                    "melancholic yet beautiful scenes",
                    "cozy warm intimate spaces",
                    "tense claustrophobic dark scenes",
                    "whimsical dreamy atmosphere"
                ]
            },
            {
                "category": "Cinematography",
                "queries": [
                    "symmetrical compositions centered framing",
                    "wide landscape shots with tiny people",
                    "harsh black and white contrast",
                    "minimalist stark compositions"
                ]
            },
            {
                "category": "Seasonal",
                "queries": [
                    "autumn colors and falling leaves",
                    "cherry blossoms and spring pink",
                    "summer beach golden hour",
                    "winter snow and cold blues"
                ]
            }
        ]
    }
