"""
Social Features Pydantic schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.schemas.common import TimestampMixin
from app.schemas.user import UserResponse
from app.schemas.movie import MovieResponse


class UserFollowRequest(BaseModel):
    """Schema for following a user."""
    user_id: UUID


class UserFollowResponse(BaseModel):
    """Schema for user follow relationship."""
    follower_id: UUID
    following_id: UUID
    followed_at: datetime
    
    class Config:
        from_attributes = True


class UserFollowWithProfile(UserFollowResponse):
    """Follow relationship with user profile."""
    user: UserResponse


class FollowersListResponse(BaseModel):
    """Schema for followers list."""
    followers: List[UserResponse]
    total_count: int


class FollowingListResponse(BaseModel):
    """Schema for following list."""
    following: List[UserResponse]
    total_count: int


class UserListCreate(BaseModel):
    """Schema for creating a user list."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_public: bool = True


class UserListUpdate(BaseModel):
    """Schema for updating a user list."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_public: Optional[bool] = None


class UserListResponse(TimestampMixin):
    """Schema for user list response."""
    id: int
    user_id: UUID
    name: str
    description: Optional[str]
    is_public: bool
    items_count: int
    likes_count: int
    
    class Config:
        from_attributes = True


class UserListWithItems(UserListResponse):
    """User list with movie items."""
    movies: List[MovieResponse]


class ListItemAdd(BaseModel):
    """Schema for adding item to list."""
    list_id: int
    movie_id: int
    notes: Optional[str] = Field(None, max_length=500)


class CollaborativeListInvite(BaseModel):
    """Schema for inviting user to collaborative list."""
    list_id: int
    user_id: UUID
    can_edit: bool = False


class ActivityFeedItem(BaseModel):
    """Schema for activity feed item."""
    id: int
    user_id: UUID
    username: str
    user_avatar: Optional[str]
    activity_type: str  # 'rating', 'review', 'watchlist_add', 'list_create', etc.
    movie_id: Optional[int]
    movie_title: Optional[str]
    content: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ActivityFeedResponse(BaseModel):
    """Schema for activity feed."""
    activities: List[ActivityFeedItem]
    total_count: int
    has_more: bool


class SocialStatsResponse(BaseModel):
    """Schema for user social statistics."""
    followers_count: int
    following_count: int
    lists_count: int
    public_lists_count: int
    total_list_likes: int
    activity_count: int
