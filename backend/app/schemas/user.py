"""
User-related Pydantic schemas.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.schemas.common import TimestampMixin


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        """Ensure password meets security requirements."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response."""
    id: UUID
    email: EmailStr
    username: str
    full_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    is_verified: bool
    is_premium: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfileResponse(UserResponse):
    """Extended user profile with statistics."""
    ratings_count: int = 0
    reviews_count: int = 0
    watchlist_count: int = 0
    followers_count: int = 0
    following_count: int = 0


class UserPreferencesUpdate(BaseModel):
    """Schema for updating user preferences."""
    favorite_genres: Optional[List[str]] = None
    disliked_genres: Optional[List[str]] = None
    favorite_decades: Optional[List[str]] = None
    preferred_languages: Optional[List[str]] = None
    preferred_moods: Optional[List[str]] = None
    diversity_preference: Optional[int] = Field(None, ge=1, le=10)
    include_adult_content: Optional[bool] = None
    min_rating_threshold: Optional[int] = Field(None, ge=0, le=10)
    max_runtime_minutes: Optional[int] = Field(None, ge=0, le=300)
    enable_llm_recommendations: Optional[bool] = None
    enable_aesthetic_search: Optional[bool] = None
    enable_gnn_recommendations: Optional[bool] = None


class UserPreferencesResponse(BaseModel):
    """Schema for user preferences response."""
    favorite_genres: List[str]
    disliked_genres: List[str]
    favorite_decades: List[str]
    preferred_languages: List[str]
    preferred_moods: List[str]
    diversity_preference: int
    include_adult_content: bool
    min_rating_threshold: int
    max_runtime_minutes: Optional[int]
    enable_llm_recommendations: bool
    enable_aesthetic_search: bool
    enable_gnn_recommendations: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""
    sub: str  # user_id
    exp: int
    iat: int
    type: str  # "access" or "refresh"


class PasswordChange(BaseModel):
    """Schema for password change."""
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @validator('new_password')
    def validate_password(cls, v, values):
        """Ensure new password is different and meets requirements."""
        if 'old_password' in values and v == values['old_password']:
            raise ValueError('New password must be different from old password')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v


class EmailVerificationRequest(BaseModel):
    """Schema for email verification."""
    token: str


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)
