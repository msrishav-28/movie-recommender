"""
Evaluation Metrics - Production Grade
Comprehensive metrics suite for recommendation system evaluation.
Implements RMSE, MAE, Precision@K, Recall@K, NDCG, MAP, diversity, serendipity.
"""

from typing import List, Dict, Any, Set
import numpy as np
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class RecommendationMetrics:
    """
    Comprehensive evaluation metrics for recommendation systems.
    
    Metrics implemented:
    - RMSE (Root Mean Squared Error)
    - MAE (Mean Absolute Error)
    - Precision@K
    - Recall@K
    - NDCG (Normalized Discounted Cumulative Gain)
    - MAP (Mean Average Precision)
    - Diversity Score
    - Serendipity Score
    - Coverage
    - Novelty
    """
    
    @staticmethod
    def rmse(predictions: List[float], actuals: List[float]) -> float:
        """
        Calculate Root Mean Squared Error.
        
        Args:
            predictions: Predicted ratings
            actuals: Actual ratings
        
        Returns:
            RMSE value
        """
        predictions = np.array(predictions)
        actuals = np.array(actuals)
        
        mse = np.mean((predictions - actuals) ** 2)
        return float(np.sqrt(mse))
    
    @staticmethod
    def mae(predictions: List[float], actuals: List[float]) -> float:
        """
        Calculate Mean Absolute Error.
        
        Args:
            predictions: Predicted ratings
            actuals: Actual ratings
        
        Returns:
            MAE value
        """
        predictions = np.array(predictions)
        actuals = np.array(actuals)
        
        return float(np.mean(np.abs(predictions - actuals)))
    
    @staticmethod
    def precision_at_k(
        recommended: List[int],
        relevant: Set[int],
        k: int
    ) -> float:
        """
        Calculate Precision@K.
        
        Args:
            recommended: List of recommended item IDs
            relevant: Set of relevant item IDs
            k: Cut-off value
        
        Returns:
            Precision@K value
        """
        if k == 0:
            return 0.0
        
        recommended_at_k = recommended[:k]
        relevant_recommended = sum(1 for item in recommended_at_k if item in relevant)
        
        return relevant_recommended / k
    
    @staticmethod
    def recall_at_k(
        recommended: List[int],
        relevant: Set[int],
        k: int
    ) -> float:
        """
        Calculate Recall@K.
        
        Args:
            recommended: List of recommended item IDs
            relevant: Set of relevant item IDs
            k: Cut-off value
        
        Returns:
            Recall@K value
        """
        if len(relevant) == 0:
            return 0.0
        
        recommended_at_k = recommended[:k]
        relevant_recommended = sum(1 for item in recommended_at_k if item in relevant)
        
        return relevant_recommended / len(relevant)
    
    @staticmethod
    def ndcg_at_k(
        recommended: List[int],
        relevance_scores: Dict[int, float],
        k: int
    ) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain@K.
        
        Args:
            recommended: List of recommended item IDs
            relevance_scores: Dictionary of item_id -> relevance score
            k: Cut-off value
        
        Returns:
            NDCG@K value
        """
        def dcg(scores: List[float]) -> float:
            """Calculate DCG."""
            return sum(
                (2 ** score - 1) / np.log2(idx + 2)
                for idx, score in enumerate(scores)
            )
        
        # Get relevance scores for recommended items
        recommended_at_k = recommended[:k]
        actual_scores = [relevance_scores.get(item, 0.0) for item in recommended_at_k]
        
        # Calculate DCG
        dcg_value = dcg(actual_scores)
        
        # Calculate ideal DCG (sorted by relevance)
        ideal_scores = sorted(relevance_scores.values(), reverse=True)[:k]
        idcg_value = dcg(ideal_scores)
        
        if idcg_value == 0:
            return 0.0
        
        return dcg_value / idcg_value
    
    @staticmethod
    def mean_average_precision(
        recommended: List[int],
        relevant: Set[int],
        k: int = None
    ) -> float:
        """
        Calculate Mean Average Precision.
        
        Args:
            recommended: List of recommended item IDs
            relevant: Set of relevant item IDs
            k: Optional cut-off value
        
        Returns:
            MAP value
        """
        if not relevant:
            return 0.0
        
        if k:
            recommended = recommended[:k]
        
        relevant_count = 0
        precision_sum = 0.0
        
        for idx, item in enumerate(recommended):
            if item in relevant:
                relevant_count += 1
                precision_sum += relevant_count / (idx + 1)
        
        if relevant_count == 0:
            return 0.0
        
        return precision_sum / min(len(relevant), len(recommended))
    
    @staticmethod
    def diversity_score(
        recommendations: List[Dict[str, Any]],
        similarity_matrix: Dict[tuple, float] = None
    ) -> float:
        """
        Calculate diversity score (intra-list dissimilarity).
        
        Args:
            recommendations: List of recommended items with metadata
            similarity_matrix: Optional pre-computed similarity matrix
        
        Returns:
            Diversity score (0-1, higher = more diverse)
        """
        if len(recommendations) <= 1:
            return 0.0
        
        # Calculate pairwise dissimilarity
        dissimilarities = []
        
        for i in range(len(recommendations)):
            for j in range(i + 1, len(recommendations)):
                item_i = recommendations[i]
                item_j = recommendations[j]
                
                # Use similarity matrix if provided
                if similarity_matrix:
                    key = (item_i.get("movie_id"), item_j.get("movie_id"))
                    similarity = similarity_matrix.get(key, 0.0)
                else:
                    # Calculate genre-based similarity as fallback
                    genres_i = set(item_i.get("metadata", {}).get("genres", []))
                    genres_j = set(item_j.get("metadata", {}).get("genres", []))
                    
                    if genres_i and genres_j:
                        similarity = len(genres_i & genres_j) / len(genres_i | genres_j)
                    else:
                        similarity = 0.0
                
                dissimilarities.append(1.0 - similarity)
        
        return float(np.mean(dissimilarities))
    
    @staticmethod
    def serendipity_score(
        recommendations: List[Dict[str, Any]],
        user_profile: Dict[str, Any]
    ) -> float:
        """
        Calculate serendipity score (unexpected but relevant).
        
        Args:
            recommendations: List of recommended items
            user_profile: User's profile with preferences
        
        Returns:
            Serendipity score (0-1)
        """
        if not recommendations:
            return 0.0
        
        user_genres = set(user_profile.get("favorite_genres", []))
        
        serendipitous_count = 0
        for rec in recommendations:
            rec_genres = set(rec.get("metadata", {}).get("genres", []))
            
            # Serendipitous if high score but outside usual genres
            if rec.get("score", 0) > 0.7:
                overlap = len(user_genres & rec_genres)
                if overlap <= 1:  # Minimal genre overlap
                    serendipitous_count += 1
        
        return serendipitous_count / len(recommendations)
    
    @staticmethod
    def catalog_coverage(
        recommended_items: Set[int],
        total_catalog_size: int
    ) -> float:
        """
        Calculate catalog coverage.
        
        Args:
            recommended_items: Set of all recommended item IDs
            total_catalog_size: Total number of items in catalog
        
        Returns:
            Coverage ratio (0-1)
        """
        if total_catalog_size == 0:
            return 0.0
        
        return len(recommended_items) / total_catalog_size
    
    @staticmethod
    def novelty_score(
        recommendations: List[Dict[str, Any]],
        item_popularity: Dict[int, int]
    ) -> float:
        """
        Calculate novelty score (recommending less popular items).
        
        Args:
            recommendations: List of recommended items
            item_popularity: Dictionary of item_id -> popularity count
        
        Returns:
            Novelty score (higher = more novel)
        """
        if not recommendations:
            return 0.0
        
        total_popularity = sum(item_popularity.values())
        
        novelties = []
        for rec in recommendations:
            item_id = rec.get("movie_id")
            popularity = item_popularity.get(item_id, 1)
            
            # Novelty is inverse of popularity
            novelty = 1.0 - (popularity / total_popularity) if total_popularity > 0 else 1.0
            novelties.append(novelty)
        
        return float(np.mean(novelties))
    
    @staticmethod
    def evaluate_batch(
        user_recommendations: Dict[str, List[int]],
        user_relevant_items: Dict[str, Set[int]],
        k: int = 20
    ) -> Dict[str, float]:
        """
        Evaluate recommendations for multiple users.
        
        Args:
            user_recommendations: Dict of user_id -> recommended item IDs
            user_relevant_items: Dict of user_id -> relevant item IDs
            k: Cut-off value
        
        Returns:
            Dictionary of aggregated metrics
        """
        precisions = []
        recalls = []
        
        for user_id, recommended in user_recommendations.items():
            relevant = user_relevant_items.get(user_id, set())
            
            if relevant:
                precision = RecommendationMetrics.precision_at_k(recommended, relevant, k)
                recall = RecommendationMetrics.recall_at_k(recommended, relevant, k)
                
                precisions.append(precision)
                recalls.append(recall)
        
        # Calculate F1 score
        avg_precision = np.mean(precisions) if precisions else 0.0
        avg_recall = np.mean(recalls) if recalls else 0.0
        
        f1 = 0.0
        if avg_precision + avg_recall > 0:
            f1 = 2 * (avg_precision * avg_recall) / (avg_precision + avg_recall)
        
        return {
            "precision@k": float(avg_precision),
            "recall@k": float(avg_recall),
            "f1@k": float(f1),
            "num_users": len(user_recommendations)
        }
    
    @staticmethod
    def generate_report(
        recommendations: List[Dict[str, Any]],
        relevant_items: Set[int],
        user_profile: Dict[str, Any],
        k: int = 20
    ) -> Dict[str, Any]:
        """
        Generate comprehensive evaluation report.
        
        Args:
            recommendations: List of recommendations
            relevant_items: Set of relevant items
            user_profile: User profile data
            k: Cut-off value
        
        Returns:
            Complete metrics report
        """
        recommended_ids = [rec.get("movie_id") for rec in recommendations]
        
        return {
            "precision@k": RecommendationMetrics.precision_at_k(recommended_ids, relevant_items, k),
            "recall@k": RecommendationMetrics.recall_at_k(recommended_ids, relevant_items, k),
            "diversity": RecommendationMetrics.diversity_score(recommendations),
            "serendipity": RecommendationMetrics.serendipity_score(recommendations, user_profile),
            "num_recommendations": len(recommendations),
            "num_relevant": len(relevant_items),
            "coverage": len(set(recommended_ids)) / len(recommended_ids) if recommended_ids else 0
        }
