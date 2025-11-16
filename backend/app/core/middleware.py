"""
Custom middleware for request processing, timing, CORS, rate limiting, etc.
Production-grade middleware with comprehensive logging and monitoring.
"""

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import uuid
from typing import Callable
import logging

from app.core.config import settings
from app.core.logging import RequestLogger
from app.cache.redis_client import get_redis_client

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Add unique request ID to each request.
    Useful for tracing requests across microservices.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Add to request state
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Measure and log request processing time.
    Adds timing information to response headers.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Add timing header
        response.headers["X-Process-Time"] = f"{duration:.2f}ms"
        
        # Log request/response
        request_id = getattr(request.state, "request_id", "unknown")
        user_id = getattr(request.state, "user_id", None)
        
        RequestLogger.log_request(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            user_id=user_id
        )
        
        RequestLogger.log_response(
            request_id=request_id,
            status_code=response.status_code,
            duration_ms=duration
        )
        
        # Log slow requests
        if duration > 1000:  # Log if request takes more than 1 second
            logger.warning(
                f"Slow request detected",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration,
                    "user_id": user_id
                }
            )
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using Redis.
    Limits requests per minute and per hour.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.redis_client = None
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting if disabled
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
        
        # Skip for health checks and metrics
        if request.url.path in ["/health", "/metrics", "/docs", "/redoc"]:
            return await call_next(request)
        
        # Initialize Redis client if not done
        if not self.redis_client:
            self.redis_client = get_redis_client(db=settings.REDIS_DB_RATE_LIMIT)
        
        # Get identifier (user ID or IP address)
        user_id = getattr(request.state, "user_id", None)
        identifier = user_id or request.client.host
        
        # Check rate limits
        is_allowed, retry_after = await self._check_rate_limit(
            identifier=identifier,
            path=request.url.path
        )
        
        if not is_allowed:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "message": "Rate limit exceeded",
                        "type": "RateLimitError",
                        "details": {"retry_after": retry_after}
                    }
                },
                headers={"Retry-After": str(retry_after)}
            )
        
        return await call_next(request)
    
    async def _check_rate_limit(self, identifier: str, path: str) -> tuple[bool, int]:
        """
        Check if request is within rate limits.
        Returns (is_allowed, retry_after_seconds)
        """
        # Rate limit keys
        minute_key = f"rate_limit:minute:{identifier}:{path}"
        hour_key = f"rate_limit:hour:{identifier}:{path}"
        
        try:
            # Check minute limit
            minute_count = await self.redis_client.incr(minute_key)
            if minute_count == 1:
                await self.redis_client.expire(minute_key, 60)
            
            if minute_count > settings.RATE_LIMIT_PER_MINUTE:
                ttl = await self.redis_client.ttl(minute_key)
                return False, ttl
            
            # Check hour limit
            hour_count = await self.redis_client.incr(hour_key)
            if hour_count == 1:
                await self.redis_client.expire(hour_key, 3600)
            
            if hour_count > settings.RATE_LIMIT_PER_HOUR:
                ttl = await self.redis_client.ttl(hour_key)
                return False, ttl
            
            return True, 0
            
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            # Fail open - allow request if Redis is down
            return True, 0


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Catch and handle errors, ensuring proper logging.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            request_id = getattr(request.state, "request_id", "unknown")
            user_id = getattr(request.state, "user_id", None)
            
            RequestLogger.log_error(
                request_id=request_id,
                error=e,
                user_id=user_id
            )
            
            # Re-raise to let exception handlers deal with it
            raise


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response


class UserContextMiddleware(BaseHTTPMiddleware):
    """
    Extract user context from JWT token and add to request state.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
            try:
                from app.core.security import decode_token
                payload = decode_token(token)
                
                # Add user context to request state
                request.state.user_id = payload.get("sub")
                request.state.user_email = payload.get("email")
                request.state.user_roles = payload.get("roles", [])
                
            except Exception as e:
                # Don't fail if token is invalid - let route handlers deal with it
                logger.debug(f"Failed to decode token: {e}")
        
        return await call_next(request)


class CompressionMiddleware(GZipMiddleware):
    """
    Compress responses with GZip.
    Configured for optimal compression.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app, minimum_size=500, compresslevel=6)


def setup_middleware(app):
    """
    Register all middleware with the FastAPI application.
    Order matters - first added is outermost layer.
    """
    
    # CORS - must be first
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Process-Time"]
    )
    
    # Trusted Host - security
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS
        )
    
    # Security Headers
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Compression
    app.add_middleware(CompressionMiddleware)
    
    # Request ID
    app.add_middleware(RequestIDMiddleware)
    
    # User Context
    app.add_middleware(UserContextMiddleware)
    
    # Timing
    app.add_middleware(TimingMiddleware)
    
    # Rate Limiting
    app.add_middleware(RateLimitMiddleware)
    
    # Error Handling - should be last
    app.add_middleware(ErrorHandlingMiddleware)
    
    logger.info("All middleware registered successfully")
