"""
Redis client wrapper with connection pooling and error handling.
"""

import redis.asyncio as redis
from typing import Optional, Any
import json
import logging
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.exceptions import CacheError

logger = logging.getLogger(__name__)


class RedisClient:
    """Async Redis client with connection pooling."""
    
    def __init__(self, db: int = 0):
        """
        Initialize Redis client.
        
        Args:
            db: Redis database number (0-15)
        """
        self.db = db
        self._client: Optional[redis.Redis] = None
        self._pool: Optional[redis.ConnectionPool] = None
    
    async def connect(self):
        """Establish Redis connection."""
        if self._client is None:
            try:
                self._pool = redis.ConnectionPool.from_url(
                    settings.REDIS_URL,
                    db=self.db,
                    max_connections=settings.REDIS_MAX_CONNECTIONS,
                    socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
                    socket_connect_timeout=settings.REDIS_SOCKET_CONNECT_TIMEOUT,
                    decode_responses=True
                )
                self._client = redis.Redis(connection_pool=self._pool)
                await self._client.ping()
                logger.info(f"Connected to Redis DB {self.db}")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise CacheError(f"Redis connection failed: {e}")
    
    async def disconnect(self):
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            if self._pool:
                await self._pool.disconnect()
            self._client = None
            self._pool = None
            logger.info(f"Disconnected from Redis DB {self.db}")
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key."""
        try:
            if not self._client:
                await self.connect()
            value = await self._client.get(key)
            return value
        except Exception as e:
            logger.error(f"Redis GET error for key {key}: {e}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set key-value pair.
        
        Args:
            key: Cache key
            value: Value to store
            ttl: Time to live in seconds
        
        Returns:
            True if successful
        """
        try:
            if not self._client:
                await self.connect()
            
            if ttl:
                await self._client.setex(key, ttl, value)
            else:
                await self._client.set(key, value)
            return True
        except Exception as e:
            logger.error(f"Redis SET error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key."""
        try:
            if not self._client:
                await self.connect()
            await self._client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis DELETE error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        try:
            if not self._client:
                await self.connect()
            return await self._client.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis EXISTS error for key {key}: {e}")
            return False
    
    async def incr(self, key: str) -> int:
        """Increment key value."""
        try:
            if not self._client:
                await self.connect()
            return await self._client.incr(key)
        except Exception as e:
            logger.error(f"Redis INCR error for key {key}: {e}")
            raise CacheError(f"Failed to increment key: {e}")
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Set key expiration."""
        try:
            if not self._client:
                await self.connect()
            return await self._client.expire(key, seconds)
        except Exception as e:
            logger.error(f"Redis EXPIRE error for key {key}: {e}")
            return False
    
    async def ttl(self, key: str) -> int:
        """Get remaining TTL for key."""
        try:
            if not self._client:
                await self.connect()
            return await self._client.ttl(key)
        except Exception as e:
            logger.error(f"Redis TTL error for key {key}: {e}")
            return -1
    
    async def get_json(self, key: str) -> Optional[dict]:
        """Get JSON value."""
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for key {key}: {e}")
        return None
    
    async def set_json(
        self,
        key: str,
        value: dict,
        ttl: Optional[int] = None
    ) -> bool:
        """Set JSON value."""
        try:
            json_str = json.dumps(value)
            return await self.set(key, json_str, ttl)
        except Exception as e:
            logger.error(f"JSON encode error for key {key}: {e}")
            return False
    
    async def keys(self, pattern: str) -> list:
        """Get keys matching pattern."""
        try:
            if not self._client:
                await self.connect()
            return await self._client.keys(pattern)
        except Exception as e:
            logger.error(f"Redis KEYS error for pattern {pattern}: {e}")
            return []
    
    async def flushdb(self):
        """Clear current database."""
        try:
            if not self._client:
                await self.connect()
            await self._client.flushdb()
            logger.warning(f"Flushed Redis DB {self.db}")
        except Exception as e:
            logger.error(f"Redis FLUSHDB error: {e}")
            raise CacheError(f"Failed to flush database: {e}")


# Singleton instances for different databases
_redis_clients = {}


def get_redis_client(db: int = 0) -> RedisClient:
    """
    Get Redis client for specific database.
    
    Args:
        db: Database number (0-15)
    
    Returns:
        RedisClient instance
    """
    if db not in _redis_clients:
        _redis_clients[db] = RedisClient(db)
    return _redis_clients[db]


# Pre-configured clients for specific use cases
def get_cache_client() -> RedisClient:
    """Get Redis client for caching."""
    return get_redis_client(settings.REDIS_DB_CACHE)


def get_session_client() -> RedisClient:
    """Get Redis client for sessions."""
    return get_redis_client(settings.REDIS_DB_SESSIONS)


def get_rate_limit_client() -> RedisClient:
    """Get Redis client for rate limiting."""
    return get_redis_client(settings.REDIS_DB_RATE_LIMIT)


async def close_all_redis_connections():
    """Close all Redis connections."""
    for client in _redis_clients.values():
        await client.disconnect()
    _redis_clients.clear()
    logger.info("All Redis connections closed")
