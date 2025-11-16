"""
CLIP-based Semantic Aesthetic Search Engine - Production Grade
Enables searching movies by visual aesthetics, mood, and cinematography.
World's first implementation of "rain with pink skies" style queries.
"""

from typing import List, Dict, Any, Optional
import asyncio
import time
import torch
import numpy as np
from transformers import CLIPModel, CLIPProcessor
from PIL import Image
import logging
from collections import defaultdict

from app.core.config import settings
from app.core.exceptions import MLModelError, PineconeError
from app.core.logging import MLLogger
from app.cache.cache_manager import CacheManager
from app.vector_db.pinecone_client import get_pinecone_client
from app.ml.semantic_search.query_parser import AestheticQueryParser
from app.ml.semantic_search.color_analyzer import ColorAnalyzer

logger = logging.getLogger(__name__)


class AestheticSearchResult:
    """Single aesthetic search result."""
    
    def __init__(
        self,
        movie_id: int,
        score: float,
        matching_frames: List[Dict[str, Any]],
        visual_summary: Dict[str, Any],
        metadata: Dict[str, Any]
    ):
        self.movie_id = movie_id
        self.score = score
        self.matching_frames = matching_frames
        self.visual_summary = visual_summary
        self.metadata = metadata
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "movie_id": self.movie_id,
            "score": round(self.score, 4),
            "num_matching_frames": len(self.matching_frames),
            "best_frames": self.matching_frames[:3],  # Top 3 frames
            "visual_summary": self.visual_summary,
            "metadata": self.metadata
        }


class CLIPAestheticSearchEngine:
    """
    CLIP-based semantic search engine for visual aesthetics.
    
    Capabilities:
    - Text-to-image similarity search
    - Color palette matching
    - Weather/time-of-day filtering
    - Visual element detection
    - Mood/atmosphere matching
    - Cinematography style matching
    
    Examples:
    - "rain with pink skies and neon lights"
    - "warm autumn colors in countryside"
    - "symmetrical compositions with pastel colors"
    - "melancholic urban scenes at night"
    """
    
    def __init__(self):
        """Initialize CLIP model and supporting components."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load CLIP model
        logger.info(f"Loading CLIP model: {settings.MODEL_CLIP_PATH}")
        self.clip_model = CLIPModel.from_pretrained(settings.MODEL_CLIP_PATH).to(self.device)
        self.clip_processor = CLIPProcessor.from_pretrained(settings.MODEL_CLIP_PATH)
        self.clip_model.eval()  # Set to evaluation mode
        
        # Supporting components
        self.query_parser = AestheticQueryParser()
        self.color_analyzer = ColorAnalyzer()
        self.cache_manager = CacheManager()
        
        # Pinecone client
        self.pinecone_client = get_pinecone_client()
        self.index = self.pinecone_client.Index(settings.PINECONE_INDEX_AESTHETIC)
        
        logger.info(f"CLIPAestheticSearchEngine initialized on {self.device}")
    
    async def search_by_aesthetic(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 20,
        min_score: Optional[float] = None
    ) -> List[AestheticSearchResult]:
        """
        Search movies by aesthetic description.
        
        Args:
            query: Natural language aesthetic query
                   Examples: "rain with pink skies", "warm autumn colors"
            filters: Additional filters (genre, year, etc.)
            top_k: Number of results to return
            min_score: Minimum similarity score (0-1)
        
        Returns:
            List of AestheticSearchResult objects
        """
        start_time = time.time()
        
        try:
            # Check cache
            cache_key = self._get_cache_key(query, filters, top_k)
            cached = await self.cache_manager.get(cache_key)
            if cached:
                logger.info(f"Returning cached aesthetic search for: '{query}'")
                return [AestheticSearchResult(**r) for r in cached]
            
            logger.info(f"Aesthetic search query: '{query}'")
            
            # Step 1: Convert query text to CLIP embedding
            query_embedding = await self._text_to_embedding(query)
            
            # Step 2: Parse query for structured filters
            parsed_filters = self.query_parser.parse_query(query)
            
            # Step 3: Merge with user-provided filters
            final_filters = self._merge_filters(parsed_filters, filters)
            
            # Step 4: Search Pinecone vector database
            search_results = await self._search_vectors(
                query_embedding=query_embedding,
                filters=final_filters,
                top_k=top_k * 5  # Get more for post-filtering
            )
            
            # Step 5: Group by movie and aggregate scores
            movie_results = self._aggregate_by_movie(search_results)
            
            # Step 6: Filter by minimum score
            min_threshold = min_score or settings.AESTHETIC_MIN_SCORE
            filtered_results = [
                r for r in movie_results
                if r.score >= min_threshold
            ]
            
            # Step 7: Sort and limit
            filtered_results.sort(key=lambda x: x.score, reverse=True)
            final_results = filtered_results[:top_k]
            
            # Cache results
            await self.cache_manager.set(
                cache_key,
                [r.to_dict() for r in final_results],
                ttl=settings.CACHE_SEARCH_RESULTS_TTL
            )
            
            # Log metrics
            duration_ms = (time.time() - start_time) * 1000
            MLLogger.log_prediction(
                model_name="CLIPAestheticSearch",
                user_id="anonymous",  # No user context in search
                duration_ms=duration_ms,
                num_results=len(final_results)
            )
            
            logger.info(
                f"Aesthetic search completed: found {len(final_results)} movies "
                f"matching '{query}' in {duration_ms:.2f}ms"
            )
            
            return final_results
            
        except Exception as e:
            MLLogger.log_model_error("CLIPAestheticSearch", e)
            raise MLModelError("CLIPAestheticSearch", str(e))
    
    async def search_by_color_palette(
        self,
        colors: List[str],
        tolerance: float = 0.1,
        top_k: int = 20
    ) -> List[AestheticSearchResult]:
        """
        Search movies by specific color palette.
        
        Args:
            colors: List of hex color codes (e.g., ['#FF5733', '#C70039'])
            tolerance: Color matching tolerance (0-1)
            top_k: Number of results
        
        Returns:
            Matching movies
        """
        logger.info(f"Color palette search: {colors}")
        
        # Convert hex colors to LAB color space for better matching
        lab_colors = [self.color_analyzer.hex_to_lab(c) for c in colors]
        
        # Build filter for Pinecone
        color_filter = {
            "dominant_colors": {
                "$in": colors
            }
        }
        
        # Use empty embedding (will filter by metadata only)
        results = await self._search_vectors(
            query_embedding=None,
            filters=color_filter,
            top_k=top_k * 3
        )
        
        # Further refine with color distance
        refined_results = []
        for result in results:
            movie_colors = result.get("dominant_colors", [])
            distance = self.color_analyzer.calculate_color_distance(lab_colors, movie_colors)
            
            if distance <= tolerance:
                result["color_distance"] = distance
                refined_results.append(result)
        
        # Aggregate by movie
        movie_results = self._aggregate_by_movie(refined_results)
        movie_results.sort(key=lambda x: x.score, reverse=True)
        
        return movie_results[:top_k]
    
    async def search_by_reference_image(
        self,
        image_path: str,
        top_k: int = 20
    ) -> List[AestheticSearchResult]:
        """
        Search movies visually similar to a reference image.
        
        Args:
            image_path: Path to reference image
            top_k: Number of results
        
        Returns:
            Visually similar movies
        """
        logger.info(f"Image similarity search: {image_path}")
        
        # Load and process image
        image = Image.open(image_path).convert("RGB")
        
        # Convert image to CLIP embedding
        image_embedding = await self._image_to_embedding(image)
        
        # Search Pinecone
        results = await self._search_vectors(
            query_embedding=image_embedding,
            filters=None,
            top_k=top_k * 5
        )
        
        # Aggregate and return
        movie_results = self._aggregate_by_movie(results)
        movie_results.sort(key=lambda x: x.score, reverse=True)
        
        return movie_results[:top_k]
    
    async def _text_to_embedding(self, text: str) -> np.ndarray:
        """Convert text query to CLIP embedding."""
        
        # Process text with CLIP
        inputs = self.clip_processor(
            text=[text],
            return_tensors="pt",
            padding=True
        ).to(self.device)
        
        # Get embedding
        with torch.no_grad():
            text_features = self.clip_model.get_text_features(**inputs)
            # Normalize (important for cosine similarity)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        # Convert to numpy
        embedding = text_features.cpu().numpy()[0]
        
        return embedding
    
    async def _image_to_embedding(self, image: Image.Image) -> np.ndarray:
        """Convert image to CLIP embedding."""
        
        # Process image with CLIP
        inputs = self.clip_processor(
            images=image,
            return_tensors="pt"
        ).to(self.device)
        
        # Get embedding
        with torch.no_grad():
            image_features = self.clip_model.get_image_features(**inputs)
            # Normalize
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        # Convert to numpy
        embedding = image_features.cpu().numpy()[0]
        
        return embedding
    
    async def _search_vectors(
        self,
        query_embedding: Optional[np.ndarray],
        filters: Optional[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Search Pinecone vector database."""
        
        try:
            if query_embedding is not None:
                # Vector similarity search
                search_results = self.index.query(
                    vector=query_embedding.tolist(),
                    top_k=top_k,
                    include_metadata=True,
                    filter=filters
                )
            else:
                # Metadata-only search
                search_results = self.index.query(
                    vector=[0.0] * settings.PINECONE_DIMENSION,  # Dummy vector
                    top_k=top_k,
                    include_metadata=True,
                    filter=filters
                )
            
            # Extract results
            results = []
            for match in search_results.get("matches", []):
                results.append({
                    "movie_id": match["metadata"]["movie_id"],
                    "frame_number": match["metadata"]["frame_number"],
                    "timestamp": match["metadata"]["timestamp"],
                    "score": match["score"],
                    "frame_path": match["metadata"]["frame_path"],
                    "dominant_colors": match["metadata"].get("dominant_colors", []),
                    "visual_tags": match["metadata"].get("visual_tags", []),
                    "scene_type": match["metadata"].get("scene_type", ""),
                    "brightness": match["metadata"].get("brightness", 0.5),
                    "saturation": match["metadata"].get("saturation", 0.5)
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Pinecone search error: {e}")
            raise PineconeError(str(e))
    
    def _aggregate_by_movie(
        self,
        frame_results: List[Dict[str, Any]]
    ) -> List[AestheticSearchResult]:
        """
        Group frame results by movie and calculate aggregate scores.
        Uses max score + average of top 3 frames.
        """
        movies_dict = defaultdict(lambda: {
            "scores": [],
            "frames": [],
            "metadata": {}
        })
        
        # Group by movie
        for result in frame_results:
            movie_id = result["movie_id"]
            movies_dict[movie_id]["scores"].append(result["score"])
            movies_dict[movie_id]["frames"].append({
                "frame_number": result["frame_number"],
                "timestamp": result["timestamp"],
                "score": result["score"],
                "frame_path": result["frame_path"]
            })
            
            # Keep first metadata as representative
            if not movies_dict[movie_id]["metadata"]:
                movies_dict[movie_id]["metadata"] = {
                    "dominant_colors": result["dominant_colors"],
                    "visual_tags": result["visual_tags"],
                    "scene_type": result["scene_type"]
                }
        
        # Calculate aggregate scores
        results = []
        for movie_id, data in movies_dict.items():
            # Sort scores
            top_scores = sorted(data["scores"], reverse=True)[:3]
            
            # Aggregate: 60% max score + 40% average of top 3
            max_score = top_scores[0]
            avg_top3 = sum(top_scores) / len(top_scores)
            aggregate_score = 0.6 * max_score + 0.4 * avg_top3
            
            # Sort frames by score
            frames = sorted(data["frames"], key=lambda x: x["score"], reverse=True)
            
            # Create visual summary
            visual_summary = self._create_visual_summary(data["metadata"], frames)
            
            results.append(AestheticSearchResult(
                movie_id=movie_id,
                score=aggregate_score,
                matching_frames=frames,
                visual_summary=visual_summary,
                metadata=data["metadata"]
            ))
        
        return results
    
    def _create_visual_summary(
        self,
        metadata: Dict[str, Any],
        frames: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a visual summary of matching frames."""
        return {
            "dominant_aesthetic": metadata.get("scene_type", "unknown"),
            "color_palette": metadata.get("dominant_colors", []),
            "visual_elements": metadata.get("visual_tags", []),
            "best_match_timestamp": frames[0]["timestamp"] if frames else 0,
            "confidence": frames[0]["score"] if frames else 0.0
        }
    
    def _merge_filters(
        self,
        parsed_filters: Dict[str, Any],
        user_filters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Merge parsed query filters with user-provided filters."""
        merged = parsed_filters.copy()
        
        if user_filters:
            for key, value in user_filters.items():
                if key in merged:
                    # Merge logic (AND operation)
                    if isinstance(value, list) and isinstance(merged[key], list):
                        merged[key] = list(set(merged[key]) & set(value))
                    else:
                        merged[key] = value
                else:
                    merged[key] = value
        
        return merged
    
    def _get_cache_key(self, query: str, filters: Optional[Dict], top_k: int) -> str:
        """Generate cache key for search."""
        return f"aesthetic_search:{query}:{hash(str(filters))}:{top_k}"


# Singleton instance
_search_engine_instance = None

def get_aesthetic_search_engine() -> CLIPAestheticSearchEngine:
    """Get singleton aesthetic search engine instance."""
    global _search_engine_instance
    if _search_engine_instance is None:
        _search_engine_instance = CLIPAestheticSearchEngine()
    return _search_engine_instance
