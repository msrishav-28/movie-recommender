"""
Collaborative Filtering Engine using Surprise library.
Matrix factorization for user-based recommendations.
"""

from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split, cross_validate
from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
import logging
from pathlib import Path
import pickle

from app.core.config import settings
from app.core.exceptions import MLModelError

logger = logging.getLogger(__name__)


class CollaborativeFilteringEngine:
    """
    Collaborative filtering using SVD (Singular Value Decomposition).
    Predicts ratings based on similar users' preferences.
    """
    
    def __init__(self):
        self.model = None
        self.model_path = Path(settings.MODEL_COLLABORATIVE_PATH)
        self.trainset = None
        self.is_trained = False
    
    def train(
        self,
        ratings_df: pd.DataFrame,
        n_factors: int = 100,
        n_epochs: int = 20,
        lr_all: float = 0.005,
        reg_all: float = 0.02
    ) -> Dict[str, float]:
        """
        Train collaborative filtering model.
        
        Args:
            ratings_df: DataFrame with columns [user_id, movie_id, rating]
            n_factors: Number of latent factors
            n_epochs: Number of training epochs
            lr_all: Learning rate
            reg_all: Regularization term
        
        Returns:
            Training metrics (RMSE, MAE)
        """
        try:
            logger.info("Training collaborative filtering model...")
            
            # Prepare data for Surprise
            reader = Reader(rating_scale=(0.5, 5.0))
            data = Dataset.load_from_df(
                ratings_df[['user_id', 'movie_id', 'rating']],
                reader
            )
            
            # Split into train/test
            trainset, testset = train_test_split(data, test_size=0.2)
            self.trainset = trainset
            
            # Initialize SVD model
            self.model = SVD(
                n_factors=n_factors,
                n_epochs=n_epochs,
                lr_all=lr_all,
                reg_all=reg_all,
                verbose=True
            )
            
            # Train
            self.model.fit(trainset)
            
            # Evaluate
            predictions = self.model.test(testset)
            rmse = accuracy.rmse(predictions, verbose=False)
            mae = accuracy.mae(predictions, verbose=False)
            
            self.is_trained = True
            
            logger.info(f"Model trained - RMSE: {rmse:.4f}, MAE: {mae:.4f}")
            
            return {
                "rmse": rmse,
                "mae": mae,
                "n_factors": n_factors,
                "n_epochs": n_epochs
            }
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise MLModelError("CollaborativeFiltering", f"Training failed: {e}")
    
    def cross_validate(
        self,
        ratings_df: pd.DataFrame,
        cv: int = 5
    ) -> Dict[str, Any]:
        """
        Perform cross-validation.
        
        Args:
            ratings_df: Ratings data
            cv: Number of folds
        
        Returns:
            Cross-validation results
        """
        try:
            reader = Reader(rating_scale=(0.5, 5.0))
            data = Dataset.load_from_df(
                ratings_df[['user_id', 'movie_id', 'rating']],
                reader
            )
            
            algo = SVD()
            results = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=cv, verbose=True)
            
            return {
                "rmse_mean": np.mean(results['test_rmse']),
                "rmse_std": np.std(results['test_rmse']),
                "mae_mean": np.mean(results['test_mae']),
                "mae_std": np.std(results['test_mae'])
            }
        except Exception as e:
            logger.error(f"Cross-validation failed: {e}")
            raise MLModelError("CollaborativeFiltering", f"CV failed: {e}")
    
    async def predict_rating(
        self,
        user_id: str,
        movie_id: int
    ) -> float:
        """
        Predict rating for user-movie pair.
        
        Args:
            user_id: User ID
            movie_id: Movie ID
        
        Returns:
            Predicted rating (0-5)
        """
        if not self.is_trained or self.model is None:
            logger.warning("Model not trained, returning neutral rating")
            return 3.0
        
        try:
            prediction = self.model.predict(str(user_id), str(movie_id))
            # Normalize to 0-1 for recommendation scoring
            normalized = (prediction.est - 0.5) / 4.5
            return max(0.0, min(1.0, normalized))
        except Exception as e:
            logger.error(f"Prediction failed for user {user_id}, movie {movie_id}: {e}")
            return 0.5
    
    async def get_similar_users_movies(
        self,
        user_id: str,
        k: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get movie recommendations based on similar users.
        
        Args:
            user_id: Target user ID
            k: Number of candidates to return
            filters: Additional filters
        
        Returns:
            List of candidate movies with scores
        """
        if not self.is_trained or self.model is None:
            logger.warning("Model not trained, returning empty list")
            return []
        
        try:
            # Get all movies the user hasn't rated
            # In production, this would query the database
            all_movie_ids = self._get_all_movie_ids()
            user_rated_movies = self._get_user_rated_movies(user_id)
            
            unrated_movies = [m for m in all_movie_ids if m not in user_rated_movies]
            
            # Predict ratings for unrated movies
            predictions = []
            for movie_id in unrated_movies:
                score = await self.predict_rating(user_id, movie_id)
                predictions.append({
                    "movie_id": movie_id,
                    "score": score,
                    "source": "collaborative",
                    "metadata": {}
                })
            
            # Sort by score and return top k
            predictions.sort(key=lambda x: x["score"], reverse=True)
            return predictions[:k]
            
        except Exception as e:
            logger.error(f"Failed to get recommendations: {e}")
            return []
    
    def save_model(self):
        """Save trained model to disk."""
        if not self.is_trained:
            logger.warning("No trained model to save")
            return
        
        try:
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            model_file = self.model_path / "svd_model.pkl"
            
            with open(model_file, 'wb') as f:
                pickle.dump(self.model, f)
            
            logger.info(f"Model saved to {model_file}")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
    
    def load_model(self) -> bool:
        """Load trained model from disk."""
        try:
            model_file = self.model_path / "svd_model.pkl"
            
            if not model_file.exists():
                logger.warning(f"Model file not found: {model_file}")
                return False
            
            with open(model_file, 'rb') as f:
                self.model = pickle.load(f)
            
            self.is_trained = True
            logger.info(f"Model loaded from {model_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def _get_all_movie_ids(self) -> List[int]:
        """Get all movie IDs from database (placeholder)."""
        # TODO: Query database for all movie IDs
        return list(range(1, 1001))  # Placeholder
    
    def _get_user_rated_movies(self, user_id: str) -> List[int]:
        """Get movies user has already rated (placeholder)."""
        # TODO: Query database for user's rated movies
        return []  # Placeholder


# Singleton instance
_collaborative_engine = None


def get_collaborative_engine() -> CollaborativeFilteringEngine:
    """Get singleton collaborative filtering engine."""
    global _collaborative_engine
    if _collaborative_engine is None:
        _collaborative_engine = CollaborativeFilteringEngine()
        _collaborative_engine.load_model()
    return _collaborative_engine
