"""
Watchlist Service - Business logic for watchlist operations.
"""

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
import logging

from app.db.models.watchlist import WatchlistItem
from app.schemas.watchlist import WatchlistItemCreate, WatchlistItemUpdate
from app.core.exceptions import ResourceNotFoundError, ValidationError

logger = logging.getLogger(__name__)


class WatchlistService:
    """Service for watchlist operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def add_to_watchlist(self, user_id: str, data: WatchlistItemCreate) -> WatchlistItem:
        """Add movie to watchlist."""
        # Check if already in watchlist
        existing = await self.db.execute(
            select(WatchlistItem).where(
                WatchlistItem.user_id == user_id,
                WatchlistItem.movie_id == data.movie_id
            )
        )
        if existing.scalar_one_or_none():
            raise ValidationError("Movie already in watchlist")
        
        item = WatchlistItem(
            user_id=user_id,
            movie_id=data.movie_id,
            priority=data.priority,
            notes=data.notes
        )
        
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        
        logger.info(f"Added to watchlist: user={user_id}, movie={data.movie_id}")
        return item
    
    async def remove_from_watchlist(self, user_id: str, movie_id: int):
        """Remove movie from watchlist."""
        await self.db.execute(
            delete(WatchlistItem).where(
                WatchlistItem.user_id == user_id,
                WatchlistItem.movie_id == movie_id
            )
        )
        await self.db.commit()
        logger.info(f"Removed from watchlist: user={user_id}, movie={movie_id}")
    
    async def update_watchlist_item(self, user_id: str, movie_id: int, data: WatchlistItemUpdate) -> WatchlistItem:
        """Update watchlist item."""
        result = await self.db.execute(
            select(WatchlistItem).where(
                WatchlistItem.user_id == user_id,
                WatchlistItem.movie_id == movie_id
            )
        )
        item = result.scalar_one_or_none()
        
        if not item:
            raise ResourceNotFoundError("WatchlistItem", f"{user_id}:{movie_id}")
        
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "watched" and value:
                item.watched_at = datetime.utcnow()
            setattr(item, field, value)
        
        await self.db.commit()
        await self.db.refresh(item)
        
        logger.info(f"Updated watchlist item: user={user_id}, movie={movie_id}")
        return item
    
    async def get_user_watchlist(self, user_id: str, watched: Optional[bool] = None) -> List[WatchlistItem]:
        """Get user's watchlist."""
        query = select(WatchlistItem).where(WatchlistItem.user_id == user_id)
        
        if watched is not None:
            query = query.where(WatchlistItem.watched == watched)
        
        query = query.order_by(WatchlistItem.priority.desc(), WatchlistItem.created_at.desc())
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
