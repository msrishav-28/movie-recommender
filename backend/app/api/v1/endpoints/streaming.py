"""Streaming availability endpoints."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class StreamingProvider(BaseModel):
    provider_id: int
    provider_name: str
    logo_path: Optional[str]
    

class StreamingAvailability(BaseModel):
    movie_id: int
    available: bool
    providers: List[StreamingProvider] = []
    rent_price: Optional[float] = None
    buy_price: Optional[float] = None


@router.get("/{movie_id}", response_model=StreamingAvailability)
async def get_streaming_availability(movie_id: int):
    """
    Get streaming availability for a movie.
    
    Note: This is a placeholder. Real implementation would integrate
    with JustWatch API or similar service.
    """
    
    # Placeholder response
    return StreamingAvailability(
        movie_id=movie_id,
        available=False,
        providers=[],
        rent_price=None,
        buy_price=None
    )
