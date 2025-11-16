"""
Pinecone vector database client for semantic search.
"""

import pinecone
from typing import List, Dict, Any, Optional
import logging
import numpy as np

from app.core.config import settings
from app.core.exceptions import PineconeError

logger = logging.getLogger(__name__)


class PineconeClient:
    """Client for Pinecone vector database operations."""
    
    def __init__(self):
        """Initialize Pinecone client."""
        try:
            pinecone.init(
                api_key=settings.PINECONE_API_KEY,
                environment=settings.PINECONE_ENVIRONMENT
            )
            logger.info("Pinecone client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            raise PineconeError(f"Initialization failed: {e}")
    
    def create_index(
        self,
        index_name: str,
        dimension: int,
        metric: str = "cosine"
    ):
        """
        Create Pinecone index.
        
        Args:
            index_name: Name of the index
            dimension: Vector dimension (e.g., 512 for CLIP)
            metric: Distance metric (cosine, euclidean, dotproduct)
        """
        try:
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=index_name,
                    dimension=dimension,
                    metric=metric
                )
                logger.info(f"Created Pinecone index: {index_name}")
            else:
                logger.info(f"Index {index_name} already exists")
        except Exception as e:
            logger.error(f"Failed to create index {index_name}: {e}")
            raise PineconeError(f"Index creation failed: {e}")
    
    def get_index(self, index_name: str):
        """Get Pinecone index."""
        try:
            return pinecone.Index(index_name)
        except Exception as e:
            logger.error(f"Failed to get index {index_name}: {e}")
            raise PineconeError(f"Failed to get index: {e}")
    
    async def upsert_vectors(
        self,
        index_name: str,
        vectors: List[tuple],
        namespace: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Insert or update vectors in index.
        
        Args:
            index_name: Name of the index
            vectors: List of (id, vector, metadata) tuples
            namespace: Optional namespace for organization
        
        Returns:
            Upsert statistics
        """
        try:
            index = self.get_index(index_name)
            response = index.upsert(
                vectors=vectors,
                namespace=namespace or ""
            )
            logger.info(f"Upserted {len(vectors)} vectors to {index_name}")
            return response
        except Exception as e:
            logger.error(f"Failed to upsert vectors: {e}")
            raise PineconeError(f"Upsert failed: {e}")
    
    async def query_vectors(
        self,
        index_name: str,
        query_vector: List[float],
        top_k: int = 10,
        filter: Optional[Dict[str, Any]] = None,
        namespace: Optional[str] = None,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Query similar vectors.
        
        Args:
            index_name: Name of the index
            query_vector: Query vector
            top_k: Number of results
            filter: Metadata filter
            namespace: Optional namespace
            include_metadata: Include metadata in results
        
        Returns:
            Query results with matches
        """
        try:
            index = self.get_index(index_name)
            results = index.query(
                vector=query_vector,
                top_k=top_k,
                filter=filter,
                namespace=namespace or "",
                include_metadata=include_metadata
            )
            return results
        except Exception as e:
            logger.error(f"Failed to query vectors: {e}")
            raise PineconeError(f"Query failed: {e}")
    
    async def delete_vectors(
        self,
        index_name: str,
        ids: List[str],
        namespace: Optional[str] = None
    ):
        """Delete vectors by IDs."""
        try:
            index = self.get_index(index_name)
            index.delete(ids=ids, namespace=namespace or "")
            logger.info(f"Deleted {len(ids)} vectors from {index_name}")
        except Exception as e:
            logger.error(f"Failed to delete vectors: {e}")
            raise PineconeError(f"Delete failed: {e}")
    
    async def fetch_vectors(
        self,
        index_name: str,
        ids: List[str],
        namespace: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch vectors by IDs."""
        try:
            index = self.get_index(index_name)
            return index.fetch(ids=ids, namespace=namespace or "")
        except Exception as e:
            logger.error(f"Failed to fetch vectors: {e}")
            raise PineconeError(f"Fetch failed: {e}")
    
    def get_index_stats(self, index_name: str) -> Dict[str, Any]:
        """Get index statistics."""
        try:
            index = self.get_index(index_name)
            return index.describe_index_stats()
        except Exception as e:
            logger.error(f"Failed to get index stats: {e}")
            raise PineconeError(f"Stats retrieval failed: {e}")


# Singleton instance
_pinecone_client = None


def get_pinecone_client() -> PineconeClient:
    """Get singleton Pinecone client."""
    global _pinecone_client
    if _pinecone_client is None:
        _pinecone_client = PineconeClient()
    return _pinecone_client
