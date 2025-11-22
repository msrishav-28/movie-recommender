"""
Common Pydantic schemas used across the application.
"""

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, List, Optional, Any
from datetime import datetime


T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int
    
    class Config:
        from_attributes = True


class SuccessResponse(BaseModel):
    """Standard success response."""
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


class TimestampMixin(BaseModel):
    """Mixin for created_at and updated_at fields."""
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class IDMixin(BaseModel):
    """Mixin for id field."""
    id: Any
    
    class Config:
        from_attributes = True
