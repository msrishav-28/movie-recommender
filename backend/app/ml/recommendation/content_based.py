"""
Content-Based Filtering Engine using movie metadata.
Uses TF-IDF and semantic embeddings for content similarity.
"""

from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import logging
from pathlib import Path
import pickle

from app.core.config import settings
from app.core.exceptions import MLModelError

logger = logging.getLogger(__name__)


class ContentBasedEngine:
    """
    Content-based recommendation using movie metadata.
    Recommends movies similar in plot, genre, cast, director.
    """
    
    def __init__(self):
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.movie_embeddings = None
        self.movie_id_to_idx = {}
        self.idx_to_movie_id = {}
        self.embedding_model = None
        self.is_trained = False
        self.model_path = Path(settings.MODEL_CONTENT_PATH)
    
    def train(
        self,
        movies_df: pd.DataFrame,
        use_embeddings: bool = True
    ) -> Dict[str, Any]:
        """
        Train content-based model.
        
        Args:
            movies_df: DataFrame with movie metadata (id, title, overview, genres, etc.)
            use_embeddings: Use sentence transformers for semantic embeddings
        
        Returns:
            Training metrics
        """
        try:
            logger.info("Training content-based model...")
            
            # Create content string for each movie
            movies_df['content'] = movies_df.apply(self._create_content_string, axis=1)
            
            # Create movie ID mapping
            self.movie_id_to_idx = {
                movie_id: idx for idx, movie_id in enumerate(movies_df['id'].values)
            }
            self.idx_to_movie_id = {
                idx: movie_id for movie_id, idx in self.movie_id_to_idx.items()
            }
            
            # TF-IDF approach
            logger.info("Computing TF-IDF vectors...")
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(movies_df['content'])
            
            # Semantic embeddings approach
            if use_embeddings:
                logger.info("Computing semantic embeddings...")
                self.embedding_model = SentenceTransformer('all-mpnet-base-v2')
                self.movie_embeddings = self.embedding_model.encode(
                    movies_df['content'].tolist(),
                    show_progress_bar=True,
                    batch_size=32
                )
            
            self.is_trained = True
            
            logger.info(f"Model trained with {len(movies_df)} movies")
            
            return {
                "n_movies": len(movies_df),
                "tfidf_features": self.tfidf_matrix.shape[1],
                "embedding_dim": self.movie_embeddings.shape[1] if use_embeddings else 0
            }
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            raise MLModelError("ContentBased", f"Training failed: {e}")
    
    def _create_content_string(self, row: pd.Series) -> str:
        """Create combined content string from movie metadata."""
        parts = []
        
        # Title
        if pd.notna(row.get('title')):
            parts.append(row['title'])
        
        # Overview/Plot
        if pd.notna(row.get('overview')):
            parts.append(row['overview'])
        
        # Genres (repeat for emphasis)
        if pd.notna(row.get('genres')):
            genres = row['genres'] if isinstance(row['genres'], list) else []
            parts.extend(genres * 3)
        
        # Keywords
        if pd.notna(row.get('keywords')):
            keywords = row['keywords'] if isinstance(row['keywords'], list) else []
            parts.extend(keywords * 2)
        
        # Cast
        if pd.notna(row.get('cast')):
            cast = row['cast'] if isinstance(row['cast'], list) else []
            parts.extend(cast[:5])  # Top 5 actors
        
        # Director
        if pd.notna(row.get('director')):
            parts.extend([row['director']] * 2)
        
        return ' '.join(parts)
    
    async def get_similar_movies(
        self,
        movie_id: int,
        k: int = 20,
        use_embeddings: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get movies similar to a specific movie.
        
        Args:
            movie_id: Source movie ID
            k: Number of similar movies
            use_embeddings: Use semantic embeddings vs TF-IDF
        
        Returns:
            List of similar movies with scores
        """
        if not self.is_trained:
            logger.warning("Model not trained")
            return []
        
        try:
            if movie_id not in self.movie_id_to_idx:
                logger.warning(f"Movie {movie_id} not in trained data")
                return []
            
            movie_idx = self.movie_id_to_idx[movie_id]
            
            if use_embeddings and self.movie_embeddings is not None:
                # Use semantic embeddings
                movie_vector = self.movie_embeddings[movie_idx].reshape(1, -1)
                similarities = cosine_similarity(movie_vector, self.movie_embeddings)[0]
            else:
                # Use TF-IDF
                movie_vector = self.tfidf_matrix[movie_idx]
                similarities = cosine_similarity(movie_vector, self.tfidf_matrix)[0]
            
            # Get top k similar movies (excluding itself)
            similar_indices = similarities.argsort()[::-1][1:k+1]
            
            results = []
            for idx in similar_indices:
                similar_movie_id = self.idx_to_movie_id[idx]
                score = float(similarities[idx])
                
                results.append({
                    "movie_id": similar_movie_id,
                    "score": score,
                    "source": "content_based",
                    "metadata": {"similarity_type": "embedding" if use_embeddings else "tfidf"}
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to get similar movies: {e}")
            return []
    
    async def calculate_similarity(
        self,
        user_profile: Dict[str, Any],
        movie_candidate: Dict[str, Any]
    ) -> float:
        """
        Calculate similarity between user profile and movie.
        
        Args:
            user_profile: User's taste profile
            movie_candidate: Movie to score
        
        Returns:
            Similarity score (0-1)
        """
        # Simple implementation based on genre overlap
        user_genres = set(user_profile.get("favorite_genres", []))
        movie_genres = set(movie_candidate.get("genres", []))
        
        if not user_genres or not movie_genres:
            return 0.5
        
        overlap = len(user_genres & movie_genres)
        total = len(user_genres | movie_genres)
        
        if total == 0:
            return 0.5
        
        jaccard_similarity = overlap / total
        return jaccard_similarity
    
    def save_model(self):
        """Save trained model to disk."""
        if not self.is_trained:
            logger.warning("No trained model to save")
            return
        
        try:
            self.model_path.mkdir(parents=True, exist_ok=True)
            
            # Save TF-IDF
            with open(self.model_path / "tfidf_vectorizer.pkl", 'wb') as f:
                pickle.dump(self.tfidf_vectorizer, f)
            
            with open(self.model_path / "tfidf_matrix.pkl", 'wb') as f:
                pickle.dump(self.tfidf_matrix, f)
            
            # Save embeddings
            if self.movie_embeddings is not None:
                np.save(self.model_path / "movie_embeddings.npy", self.movie_embeddings)
            
            # Save mappings
            with open(self.model_path / "mappings.pkl", 'wb') as f:
                pickle.dump({
                    "movie_id_to_idx": self.movie_id_to_idx,
                    "idx_to_movie_id": self.idx_to_movie_id
                }, f)
            
            logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
    
    def load_model(self) -> bool:
        """Load trained model from disk."""
        try:
            if not self.model_path.exists():
                logger.warning(f"Model path not found: {self.model_path}")
                return False
            
            # Load TF-IDF
            with open(self.model_path / "tfidf_vectorizer.pkl", 'rb') as f:
                self.tfidf_vectorizer = pickle.load(f)
            
            with open(self.model_path / "tfidf_matrix.pkl", 'rb') as f:
                self.tfidf_matrix = pickle.load(f)
            
            # Load embeddings
            embeddings_file = self.model_path / "movie_embeddings.npy"
            if embeddings_file.exists():
                self.movie_embeddings = np.load(embeddings_file)
                self.embedding_model = SentenceTransformer('all-mpnet-base-v2')
            
            # Load mappings
            with open(self.model_path / "mappings.pkl", 'rb') as f:
                mappings = pickle.load(f)
                self.movie_id_to_idx = mappings["movie_id_to_idx"]
                self.idx_to_movie_id = mappings["idx_to_movie_id"]
            
            self.is_trained = True
            logger.info(f"Model loaded from {self.model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False


# Singleton instance
_content_engine = None


def get_content_engine() -> ContentBasedEngine:
    """Get singleton content-based engine."""
    global _content_engine
    if _content_engine is None:
        _content_engine = ContentBasedEngine()
        _content_engine.load_model()
    return _content_engine
