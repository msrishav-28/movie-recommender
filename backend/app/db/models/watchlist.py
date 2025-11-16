"""
Watchlist and custom list models.
"""

from sqlalchemy import Column, String, Integer, Text, ForeignKey, Index, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class WatchlistItem(Base):
    """User watchlist with priority scoring."""
    
    __tablename__ = "watchlist_items"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Priority and organization
    priority = Column(Integer, default=5)  # 1-10 scale (10 = highest priority)
    is_watched = Column(Boolean, default=False, index=True)
    
    # Personal notes
    notes = Column(Text)
    tags = Column(ARRAY(String))  # Custom user tags
    
    # Why added (source)
    added_from = Column(String(100))  # recommendation, search, friend, etc.
    
    # Notifications
    notify_on_release = Column(Boolean, default=True)
    notify_on_streaming = Column(Boolean, default=True)
    
    # Timestamps
    added_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    watched_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="watchlists")
    movie = relationship("Movie", back_populates="watchlist_items")
    
    __table_args__ = (
        Index('idx_watchlist_user', 'user_id'),
        Index('idx_watchlist_movie', 'movie_id'),
        Index('idx_watchlist_priority', 'priority'),
        Index('idx_watchlist_added', 'added_at'),
        # Unique: one entry per user per movie
        Index('idx_watchlist_unique', 'user_id', 'movie_id', unique=True),
    )
    
    def __repr__(self):
        return f"<WatchlistItem user={self.user_id} movie={self.movie_id}>"


class UserList(Base):
    """Custom user-created lists."""
    
    __tablename__ = "user_lists"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # List info
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Visibility
    is_public = Column(Boolean, default=True, index=True)
    is_collaborative = Column(Boolean, default=False)  # Can others add to it?
    
    # Organization
    sort_order = Column(String(50), default='manual')  # manual, date_added, rating, release_date
    
    # Engagement
    likes_count = Column(Integer, default=0, index=True)
    comments_count = Column(Integer, default=0)
    forks_count = Column(Integer, default=0)  # How many copied this list
    
    # Forked from
    forked_from_id = Column(Integer, ForeignKey("user_lists.id", ondelete="SET NULL"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="lists")
    items = relationship("ListItem", back_populates="list", cascade="all, delete-orphan", order_by="ListItem.position")
    collaborators = relationship("ListCollaborator", back_populates="list", cascade="all, delete-orphan")
    likes = relationship("ListLike", back_populates="list", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('idx_list_user', 'user_id'),
        Index('idx_list_public', 'is_public'),
        Index('idx_list_likes', 'likes_count'),
        Index('idx_list_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<UserList '{self.name}' by user={self.user_id}>"


class ListItem(Base):
    """Items in a user list."""
    
    __tablename__ = "list_items"
    
    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey("user_lists.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Ordering
    position = Column(Integer, nullable=False)  # Manual ordering
    
    # Personal notes for this item in this list
    notes = Column(Text)
    
    # Who added it (for collaborative lists)
    added_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    
    # Timestamps
    added_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    list = relationship("UserList", back_populates="items")
    movie = relationship("Movie")
    
    __table_args__ = (
        Index('idx_list_item_list', 'list_id'),
        Index('idx_list_item_movie', 'movie_id'),
        Index('idx_list_item_position', 'position'),
        # Unique: one movie per list
        Index('idx_list_item_unique', 'list_id', 'movie_id', unique=True),
    )
    
    def __repr__(self):
        return f"<ListItem list={self.list_id} movie={self.movie_id} pos={self.position}>"


class ListCollaborator(Base):
    """Collaborators on a list."""
    
    __tablename__ = "list_collaborators"
    
    list_id = Column(Integer, ForeignKey("user_lists.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    # Permission level
    can_add = Column(Boolean, default=True)
    can_remove = Column(Boolean, default=False)
    can_edit = Column(Boolean, default=False)
    
    # Timestamps
    added_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    list = relationship("UserList", back_populates="collaborators")
    user = relationship("User")
    
    __table_args__ = (
        Index('idx_collaborator_list', 'list_id'),
        Index('idx_collaborator_user', 'user_id'),
    )


class ListLike(Base):
    """Likes on lists."""
    
    __tablename__ = "list_likes"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    list_id = Column(Integer, ForeignKey("user_lists.id", ondelete="CASCADE"), primary_key=True)
    
    liked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User")
    list = relationship("UserList", back_populates="likes")
    
    __table_args__ = (
        Index('idx_list_like_user', 'user_id'),
        Index('idx_list_like_list', 'list_id'),
    )


class WatchHistory(Base):
    """Track when users watch movies."""
    
    __tablename__ = "watch_history"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Watch details
    watched_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    watch_count = Column(Integer, default=1)  # Rewatches
    
    # Where watched
    platform = Column(String(100))  # Netflix, Theater, DVD, etc.
    
    # Relationships
    user = relationship("User")
    movie = relationship("Movie")
    
    __table_args__ = (
        Index('idx_watch_history_user', 'user_id'),
        Index('idx_watch_history_movie', 'movie_id'),
        Index('idx_watch_history_watched', 'watched_at'),
    )
    
    def __repr__(self):
        return f"<WatchHistory user={self.user_id} movie={self.movie_id} at={self.watched_at}>"
