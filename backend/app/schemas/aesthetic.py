"""
Aesthetic Search Pydantic schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class AestheticSearchRequest(BaseModel):
    """Schema for aesthetic search request."""
    query: str = Field(..., min_length=3, max_length=500, description="Natural language aesthetic query")
    filters: Optional[Dict[str, Any]] = None
    top_k: int = Field(20, ge=1, le=100)
    min_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Minimum similarity score")


class FrameMatch(BaseModel):
    """Schema for matched frame."""
    frame_number: int
    timestamp: float
    score: float
    frame_path: Optional[str]


class VisualSummary(BaseModel):
    """Schema for visual summary."""
    dominant_aesthetic: str
    color_palette: List[str]
    visual_elements: List[str]
    best_match_timestamp: float
    confidence: float


class AestheticSearchResponse(BaseModel):
    """Schema for aesthetic search result."""
    movie_id: int
    score: float
    num_matching_frames: int
    best_frames: List[FrameMatch]
    visual_summary: VisualSummary
    metadata: Optional[Dict[str, Any]] = {}


class ColorPaletteRequest(BaseModel):
    """Schema for color palette search."""
    colors: List[str] = Field(..., min_items=1, max_items=10, description="List of hex colors")
    tolerance: float = Field(0.1, ge=0.0, le=1.0, description="Color matching tolerance")
    top_k: int = Field(20, ge=1, le=100)


class ImageSimilarityRequest(BaseModel):
    """Schema for image similarity search."""
    image_path: str = Field(..., description="Path or URL to reference image")
    top_k: int = Field(20, ge=1, le=100)


class AdvancedAestheticFilters(BaseModel):
    """Schema for advanced aesthetic filters."""
    colors: Optional[List[str]] = Field(None, description="Specific colors to match")
    color_temperature: Optional[str] = Field(None, pattern=r'^(warm|cool|neutral)$')
    weather_conditions: Optional[List[str]] = None
    time_of_day: Optional[List[str]] = None
    seasons: Optional[List[str]] = None
    locations: Optional[List[str]] = None
    visual_elements: Optional[List[str]] = None
    moods: Optional[List[str]] = None
    cinematography_style: Optional[str] = None
    composition: Optional[str] = Field(None, pattern=r'^(symmetrical|rule_of_thirds|centered)$')


class AestheticTagsResponse(BaseModel):
    """Schema for available aesthetic tags."""
    colors: List[str]
    weather_conditions: List[str]
    times_of_day: List[str]
    seasons: List[str]
    locations: List[str]
    visual_elements: List[str]
    moods: List[str]
    cinematography_styles: List[str]
