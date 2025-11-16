"""
User-related database models.
Includes User, UserProfile, UserPreferences, UserSettings.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime

from app.db.database import Base


class User(Base):
    """Core user table with authentication data."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    full_name = Column(String(100))
    bio = Column(Text)
    avatar_url = Column(String(500))
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_premium = Column(Boolean, default=False, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    
    # Premium subscription
    premium_until = Column(DateTime(timezone=True))
    subscription_id = Column(String(100))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    email_verified_at = Column(DateTime(timezone=True))
    
    # Security
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True))
    
    # OAuth
    oauth_provider = Column(String(50))  # google, github, etc.
    oauth_provider_id = Column(String(255))
    
    # Relationships
    preferences = relationship("UserPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    watchlists = relationship("WatchlistItem", back_populates="user", cascade="all, delete-orphan")
    lists = relationship("UserList", back_populates="user", cascade="all, delete-orphan")
    interactions = relationship("UserInteraction", back_populates="user", cascade="all, delete-orphan")
    
    # Followers/Following
    following = relationship(
        "UserFollow",
        foreign_keys="UserFollow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan"
    )
    followers = relationship(
        "UserFollow",
        foreign_keys="UserFollow.following_id",
        back_populates="following",
        cascade="all, delete-orphan"
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_username', 'username'),
        Index('idx_user_is_premium', 'is_premium'),
        Index('idx_user_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<User {self.username}>"


class UserPreferences(Base):
    """User preferences and taste profile."""
    
    __tablename__ = "user_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # Content preferences
    favorite_genres = Column(ARRAY(String), default=list)
    disliked_genres = Column(ARRAY(String), default=list)
    favorite_decades = Column(ARRAY(String), default=list)
    preferred_languages = Column(ARRAY(String), default=list)
    
    # Mood preferences
    preferred_moods = Column(ARRAY(String), default=list)  # ['happy', 'sad', 'thrilling', etc.]
    
    # Recommendation settings
    diversity_preference = Column(Integer, default=5)  # 1-10 scale (comfort zone to exploration)
    include_adult_content = Column(Boolean, default=False)
    min_rating_threshold = Column(Integer, default=0)  # 0-10
    max_runtime_minutes = Column(Integer)
    
    # Notification preferences
    email_recommendations = Column(Boolean, default=True)
    email_new_releases = Column(Boolean, default=True)
    email_watchlist_available = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    
    # Display preferences
    language = Column(String(10), default="en")
    timezone = Column(String(50), default="UTC")
    theme = Column(String(20), default="light")  # light, dark, auto
    
    # Privacy
    profile_public = Column(Boolean, default=True)
    show_watch_history = Column(Boolean, default=True)
    show_ratings = Column(Boolean, default=True)
    show_watchlist = Column(Boolean, default=False)
    
    # Advanced ML settings
    enable_llm_recommendations = Column(Boolean, default=True)
    enable_aesthetic_search = Column(Boolean, default=True)
    enable_gnn_recommendations = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="preferences")
    
    def __repr__(self):
        return f"<UserPreferences user_id={self.user_id}>"


class UserFollow(Base):
    """User following relationships."""
    
    __tablename__ = "user_follows"
    
    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    following_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    followed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")
    
    # Indexes
    __table_args__ = (
        Index('idx_follower', 'follower_id'),
        Index('idx_following', 'following_id'),
    )
    
    def __repr__(self):
        return f"<UserFollow {self.follower_id} -> {self.following_id}>"


class UserAPIKey(Base):
    """API keys for programmatic access."""
    
    __tablename__ = "user_api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    key_hash = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Permissions
    scopes = Column(ARRAY(String), default=list)  # ['read:movies', 'write:ratings', etc.]
    
    # Rate limiting
    rate_limit_per_hour = Column(Integer, default=1000)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    
    # Indexes
    __table_args__ = (
        Index('idx_api_key_user', 'user_id'),
        Index('idx_api_key_hash', 'key_hash'),
    )
    
    def __repr__(self):
        return f"<UserAPIKey {self.name}>"


class UserSession(Base):
    """Active user sessions for tracking and security."""
    
    __tablename__ = "user_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Session data
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    refresh_token_jti = Column(String(255), unique=True)  # JWT ID for refresh token
    
    # Device/Client info
    user_agent = Column(String(500))
    ip_address = Column(String(45))
    device_type = Column(String(50))  # mobile, desktop, tablet
    browser = Column(String(50))
    os = Column(String(50))
    
    # Location
    country = Column(String(2))
    city = Column(String(100))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_session_user', 'user_id'),
        Index('idx_session_token', 'session_token'),
        Index('idx_session_active', 'is_active'),
    )
    
    def __repr__(self):
        return f"<UserSession user_id={self.user_id}>"
