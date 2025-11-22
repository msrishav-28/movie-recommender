"""
Diversity Optimizer - Production Grade
Implements Maximal Marginal Relevance (MMR) and diversity algorithms.
Prevents filter bubbles and ensures recommendation variety.
"""

from typing import List, Dict, Any, Optional
import numpy as np
import logging
from collections import defaultdict

from app.core.config import settings

logger = logging.getLogger(__name__)


class DiversityOptimizer:
    """
    Diversity optimization for recommendations.
    
    Techniques:
    - MMR (Maximal Marginal Relevance)
    - Genre diversity
    - Temporal diversity (different decades)
    - Rating diversity
    - Serendipity injection
    """
    
    def __init__(self):
        """Initialize diversity optimizer."""
        logger.info("DiversityOptimizer initialized")
    
    async def apply_mmr(
        self,
        candidates: List[Dict[str, Any]],
        lambda_param: float = 0.7,
        top_k: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Apply Maximal Marginal Relevance algorithm.
        
        MMR balances relevance and diversity:
        MMR = λ * Relevance(d) - (1-λ) * max Similarity(d, selected)
        
        Args:
            candidates: List of scored candidates
            lambda_param: Trade-off between relevance and diversity (0-1)
                         1.0 = pure relevance, 0.0 = pure diversity
            top_k: Number of results to return
        
        Returns:
            Diversified list of candidates
        """
        if not candidates:
            return []
        
        if len(candidates) <= top_k:
            return candidates
        
        logger.info(f"Applying MMR with λ={lambda_param} to {len(candidates)} candidates")
        
        # Extract candidate features for similarity computation
        candidate_features = await self._extract_features(candidates)
        
        selected = []
        remaining = list(range(len(candidates)))
        
        # Select first item (highest score)
        first_idx = 0
        selected.append(candidates[first_idx])
        remaining.remove(first_idx)
        
        # Iteratively select diverse items
        while len(selected) < top_k and remaining:
            best_mmr_score = -float('inf')
            best_idx = None
            
            for idx in remaining:
                # Relevance score (normalized)
                relevance = candidates[idx]["score"]
                
                # Maximum similarity to already selected items
                max_similarity = 0.0
                for selected_idx in [candidates.index(s) for s in selected]:
                    similarity = self._compute_similarity(
                        candidate_features[idx],
                        candidate_features[selected_idx]
                    )
                    max_similarity = max(max_similarity, similarity)
                
                # MMR score
                mmr_score = lambda_param * relevance - (1 - lambda_param) * max_similarity
                
                if mmr_score > best_mmr_score:
                    best_mmr_score = mmr_score
                    best_idx = idx
            
            if best_idx is not None:
                selected.append(candidates[best_idx])
                remaining.remove(best_idx)
        
        logger.info(f"MMR selected {len(selected)} diverse candidates")
        return selected
    
    async def ensure_genre_diversity(
        self,
        candidates: List[Dict[str, Any]],
        min_genres: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Ensure recommendations span multiple genres.
        
        Args:
            candidates: Candidate movies
            min_genres: Minimum number of different genres
        
        Returns:
            Genre-diversified candidates
        """
        genre_counts = defaultdict(int)
        diversified = []
        
        # First pass: ensure at least one from each genre
        genres_covered = set()
        
        for candidate in candidates:
            genres = candidate.get("metadata", {}).get("genres", [])
            
            if len(genres_covered) < min_genres:
                # Prioritize uncovered genres
                for genre in genres:
                    if genre not in genres_covered:
                        diversified.append(candidate)
                        genres_covered.update(genres)
                        break
            else:
                diversified.append(candidate)
        
        logger.info(f"Genre diversity: {len(genres_covered)} genres covered")
        return diversified
    
    async def inject_serendipity(
        self,
        candidates: List[Dict[str, Any]],
        serendipity_ratio: float = 0.15,
        surprise_pool: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Inject serendipitous (surprising) recommendations.
        
        Args:
            candidates: Main candidates
            serendipity_ratio: Fraction of results to be surprising (0-1)
            surprise_pool: Pool of unexpected/diverse movies
        
        Returns:
            Candidates with serendipity injection
        """
        if serendipity_ratio <= 0 or not candidates:
            return candidates
        
        num_serendipitous = int(len(candidates) * serendipity_ratio)
        
        if num_serendipitous == 0:
            return candidates
        
        # Remove lowest scoring candidates to make room
        main_candidates = candidates[:-num_serendipitous] if num_serendipitous < len(candidates) else []
        
        # Add serendipitous items (from surprise pool or generate)
        if surprise_pool:
            serendipitous = surprise_pool[:num_serendipitous]
        else:
            # Generate serendipitous candidates (placeholder)
            serendipitous = []
        
        result = main_candidates + serendipitous
        
        logger.info(f"Injected {len(serendipitous)} serendipitous recommendations")
        return result
    
    async def temporal_diversity(
        self,
        candidates: List[Dict[str, Any]],
        decades: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Ensure temporal diversity across decades.
        
        Args:
            candidates: Candidate movies
            decades: Preferred decades to cover
        
        Returns:
            Temporally diversified candidates
        """
        if not candidates:
            return candidates
        
        decade_buckets = defaultdict(list)
        
        # Group by decade
        for candidate in candidates:
            year = candidate.get("metadata", {}).get("release_year")
            if year:
                decade = (year // 10) * 10
                decade_buckets[decade].append(candidate)
        
        # Select from each decade proportionally
        diversified = []
        decades_list = sorted(decade_buckets.keys())
        
        items_per_decade = len(candidates) // max(len(decades_list), 1)
        
        for decade in decades_list:
            bucket = decade_buckets[decade]
            diversified.extend(bucket[:items_per_decade])
        
        # Fill remaining slots
        remaining = len(candidates) - len(diversified)
        if remaining > 0:
            for decade in decades_list:
                bucket = decade_buckets[decade][items_per_decade:]
                diversified.extend(bucket[:remaining])
                remaining = len(candidates) - len(diversified)
                if remaining <= 0:
                    break
        
        logger.info(f"Temporal diversity: {len(decade_buckets)} decades covered")
        return diversified[:len(candidates)]
    
    async def balance_popularity(
        self,
        candidates: List[Dict[str, Any]],
        popular_ratio: float = 0.6
    ) -> List[Dict[str, Any]]:
        """
        Balance popular and niche recommendations.
        
        Args:
            candidates: Candidate movies
            popular_ratio: Ratio of popular movies (0-1)
        
        Returns:
            Popularity-balanced candidates
        """
        if not candidates:
            return candidates
        
        # Sort by popularity
        sorted_candidates = sorted(
            candidates,
            key=lambda x: x.get("metadata", {}).get("popularity", 0),
            reverse=True
        )
        
        num_popular = int(len(candidates) * popular_ratio)
        num_niche = len(candidates) - num_popular
        
        popular = sorted_candidates[:num_popular]
        niche = sorted_candidates[num_popular:num_popular + num_niche]
        
        # Interleave for better user experience
        balanced = []
        for i in range(max(len(popular), len(niche))):
            if i < len(popular):
                balanced.append(popular[i])
            if i < len(niche):
                balanced.append(niche[i])
        
        logger.info(f"Popularity balance: {num_popular} popular, {num_niche} niche")
        return balanced[:len(candidates)]
    
    async def _extract_features(
        self,
        candidates: List[Dict[str, Any]]
    ) -> List[np.ndarray]:
        """
        Extract feature vectors for similarity computation.
        
        Features include:
        - Genres (one-hot)
        - Release year (normalized)
        - Rating
        - Popularity
        """
        features = []
        
        for candidate in candidates:
            metadata = candidate.get("metadata", {})
            
            # Genre vector (simplified)
            genres = metadata.get("genres", [])
            genre_vector = self._genres_to_vector(genres)
            
            # Year (normalized to 0-1)
            year = metadata.get("release_year", 2000)
            year_norm = (year - 1900) / 125  # Normalize to roughly 0-1
            
            # Rating (normalized to 0-1)
            rating = metadata.get("rating", 5.0) / 10.0
            
            # Popularity (normalized)
            popularity = metadata.get("popularity", 50) / 100.0
            
            # Combine features
            feature_vector = np.concatenate([
                genre_vector,
                [year_norm, rating, popularity]
            ])
            
            features.append(feature_vector)
        
        return features
    
    def _genres_to_vector(self, genres: List[str]) -> np.ndarray:
        """Convert genres to one-hot encoded vector."""
        all_genres = [
            "Action", "Adventure", "Animation", "Comedy", "Crime",
            "Documentary", "Drama", "Family", "Fantasy", "History",
            "Horror", "Music", "Mystery", "Romance", "Science Fiction",
            "TV Movie", "Thriller", "War", "Western"
        ]
        
        vector = np.zeros(len(all_genres))
        for i, genre in enumerate(all_genres):
            if genre in genres:
                vector[i] = 1.0
        
        return vector
    
    def _compute_similarity(
        self,
        features1: np.ndarray,
        features2: np.ndarray
    ) -> float:
        """Compute cosine similarity between feature vectors."""
        dot_product = np.dot(features1, features2)
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    async def calculate_diversity_metrics(
        self,
        recommendations: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Calculate diversity metrics for a recommendation list.
        
        Metrics:
        - Genre diversity (entropy)
        - Temporal spread (std dev of years)
        - Rating variance
        - Average pairwise dissimilarity
        
        Returns:
            Dictionary of diversity metrics
        """
        if not recommendations:
            return {
                "genre_diversity": 0.0,
                "temporal_spread": 0.0,
                "rating_variance": 0.0,
                "avg_dissimilarity": 0.0
            }
        
        # Genre diversity (entropy)
        genre_counts = defaultdict(int)
        for rec in recommendations:
            genres = rec.get("metadata", {}).get("genres", [])
            for genre in genres:
                genre_counts[genre] += 1
        
        total = sum(genre_counts.values())
        genre_entropy = 0.0
        if total > 0:
            for count in genre_counts.values():
                p = count / total
                if p > 0:
                    genre_entropy -= p * np.log2(p)
        
        # Temporal spread
        years = [
            rec.get("metadata", {}).get("release_year", 2000)
            for rec in recommendations
        ]
        temporal_spread = float(np.std(years))
        
        # Rating variance
        ratings = [
            rec.get("metadata", {}).get("rating", 5.0)
            for rec in recommendations
        ]
        rating_variance = float(np.var(ratings))
        
        # Average pairwise dissimilarity
        features = await self._extract_features(recommendations)
        dissimilarities = []
        for i in range(len(features)):
            for j in range(i + 1, len(features)):
                sim = self._compute_similarity(features[i], features[j])
                dissimilarities.append(1.0 - sim)
        
        avg_dissimilarity = float(np.mean(dissimilarities)) if dissimilarities else 0.0
        
        return {
            "genre_diversity": genre_entropy,
            "temporal_spread": temporal_spread,
            "rating_variance": rating_variance,
            "avg_dissimilarity": avg_dissimilarity
        }
