"""
Cache manager with multiple caching strategies.
"""

from typing import Optional, Any, Callable
import hashlib
import json
import logging
from functools import wraps

from app.cache.redis_client import get_cache_client
from app.core.config import settings

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching operations with different strategies."""
    
    def __init__(self):
        self.redis_client = get_cache_client()
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        # Create unique key from arguments
        key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
        key_hash = hashlib.md5(key_data.encode()).hexdigest()
        return f"{prefix}:{key_hash}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get cached value."""
        return await self.redis_client.get_json(key)
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Set cached value."""
        if ttl is None:
            ttl = settings.CACHE_DEFAULT_TTL
        return await self.redis_client.set_json(key, value, ttl)
    
    async def delete(self, key: str) -> bool:
        """Delete cached value."""
        return await self.redis_client.delete(key)
    
    async def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern."""
        keys = await self.redis_client.keys(pattern)
        for key in keys:
            await self.redis_client.delete(key)
        logger.info(f"Cleared {len(keys)} keys matching pattern: {pattern}")
    
    def cached(
        self,
        prefix: str,
        ttl: Optional[int] = None
    ):
        """
        Decorator for caching function results.
        
        Usage:
            @cache_manager.cached("movie_details", ttl=3600)
            async def get_movie_details(movie_id: int):
                ...
        """
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = self._generate_key(prefix, *args, **kwargs)
                
                # Try to get from cache
                cached_value = await self.get(cache_key)
                if cached_value is not None:
                    logger.debug(f"Cache HIT: {cache_key}")
                    return cached_value
                
                # Cache miss - call function
                logger.debug(f"Cache MISS: {cache_key}")
                result = await func(*args, **kwargs)
                
                # Store in cache
                await self.set(cache_key, result, ttl)
                
                return result
            
            return wrapper
        return decorator


# Singleton instance
_cache_manager = None


def get_cache_manager() -> CacheManager:
    """Get singleton cache manager."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager
