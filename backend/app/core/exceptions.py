"""
Custom exceptions and error handlers for the application.
Provides structured error responses and logging.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Custom Exception Classes
# ============================================================================

class CineAestheteException(Exception):
    """Base exception for all custom exceptions."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


# Authentication & Authorization Exceptions
class AuthenticationError(CineAestheteException):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Authentication failed", details: Dict = None):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, details)


class AuthorizationError(CineAestheteException):
    """Raised when user lacks permission."""
    def __init__(self, message: str = "Insufficient permissions", details: Dict = None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, details)


class InvalidCredentialsError(AuthenticationError):
    """Raised when credentials are invalid."""
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message)


class TokenExpiredError(AuthenticationError):
    """Raised when JWT token has expired."""
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message)


class InvalidTokenError(AuthenticationError):
    """Raised when JWT token is invalid."""
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message)


# Resource Exceptions
class ResourceNotFoundError(CineAestheteException):
    """Raised when a requested resource doesn't exist."""
    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(message, status.HTTP_404_NOT_FOUND, {"resource": resource, "id": identifier})


class ResourceAlreadyExistsError(CineAestheteException):
    """Raised when trying to create a resource that already exists."""
    def __init__(self, resource: str, identifier: Any):
        message = f"{resource} with identifier '{identifier}' already exists"
        super().__init__(message, status.HTTP_409_CONFLICT, {"resource": resource, "id": identifier})


class ResourceConflictError(CineAestheteException):
    """Raised when there's a conflict with resource state."""
    def __init__(self, message: str, details: Dict = None):
        super().__init__(message, status.HTTP_409_CONFLICT, details)


# Validation Exceptions
class ValidationError(CineAestheteException):
    """Raised when validation fails."""
    def __init__(self, message: str, field: str = None, details: Dict = None):
        details = details or {}
        if field:
            details["field"] = field
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, details)


class InvalidInputError(ValidationError):
    """Raised when input data is invalid."""
    pass


# Rate Limiting Exceptions
class RateLimitExceededError(CineAestheteException):
    """Raised when rate limit is exceeded."""
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None):
        details = {}
        if retry_after:
            details["retry_after"] = retry_after
        super().__init__(message, status.HTTP_429_TOO_MANY_REQUESTS, details)


# External Service Exceptions
class ExternalServiceError(CineAestheteException):
    """Raised when external service call fails."""
    def __init__(self, service: str, message: str = None):
        message = message or f"External service '{service}' unavailable"
        super().__init__(message, status.HTTP_503_SERVICE_UNAVAILABLE, {"service": service})


class TMDbAPIError(ExternalServiceError):
    """Raised when TMDb API fails."""
    def __init__(self, message: str = "TMDb API error"):
        super().__init__("TMDb", message)


class PineconeError(ExternalServiceError):
    """Raised when Pinecone operation fails."""
    def __init__(self, message: str = "Pinecone error"):
        super().__init__("Pinecone", message)


# ML/AI Exceptions
class MLModelError(CineAestheteException):
    """Raised when ML model operation fails."""
    def __init__(self, model_name: str, message: str = "Model error"):
        super().__init__(
            f"{model_name}: {message}",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            {"model": model_name}
        )


class ModelNotLoadedError(MLModelError):
    """Raised when trying to use a model that isn't loaded."""
    def __init__(self, model_name: str):
        super().__init__(model_name, "Model not loaded")


class PredictionError(MLModelError):
    """Raised when model prediction fails."""
    def __init__(self, model_name: str, error: str):
        super().__init__(model_name, f"Prediction failed: {error}")


# Database Exceptions
class DatabaseError(CineAestheteException):
    """Raised when database operation fails."""
    def __init__(self, message: str = "Database error", details: Dict = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, details)


class DatabaseConnectionError(DatabaseError):
    """Raised when cannot connect to database."""
    def __init__(self):
        super().__init__("Failed to connect to database")


# Cache Exceptions
class CacheError(CineAestheteException):
    """Raised when cache operation fails."""
    def __init__(self, message: str = "Cache error"):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


# Business Logic Exceptions
class BusinessLogicError(CineAestheteException):
    """Raised for business logic violations."""
    def __init__(self, message: str, details: Dict = None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, details)


class InsufficientPermissionsError(AuthorizationError):
    """Raised when user doesn't have required permissions."""
    def __init__(self, required_permission: str):
        super().__init__(
            f"Required permission: {required_permission}",
            {"required_permission": required_permission}
        )


class PremiumFeatureError(AuthorizationError):
    """Raised when non-premium user tries to access premium feature."""
    def __init__(self):
        super().__init__("This feature requires a premium subscription")


# ============================================================================
# Exception Handlers
# ============================================================================

async def cineaesthete_exception_handler(
    request: Request,
    exc: CineAestheteException
) -> JSONResponse:
    """Handle custom CineAesthete exceptions."""
    logger.error(
        f"CineAesthete Exception: {exc.message}",
        extra={
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path,
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "type": exc.__class__.__name__,
                "details": exc.details
            }
        }
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
) -> JSONResponse:
    """Handle standard HTTP exceptions."""
    logger.warning(
        f"HTTP Exception: {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "type": "HTTPException"
            }
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"][1:]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(
        "Validation Error",
        extra={
            "errors": errors,
            "path": request.url.path,
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Validation failed",
                "type": "ValidationError",
                "details": {"errors": errors}
            }
        }
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.exception(
        f"Unexpected error: {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method
        }
    )
    
    # Don't expose internal errors in production
    if settings.DEBUG:
        message = str(exc)
        error_type = exc.__class__.__name__
    else:
        message = "An unexpected error occurred"
        error_type = "InternalServerError"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": message,
                "type": error_type
            }
        }
    )


def register_exception_handlers(app):
    """Register all exception handlers with FastAPI app."""
    app.add_exception_handler(CineAestheteException, cineaesthete_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
