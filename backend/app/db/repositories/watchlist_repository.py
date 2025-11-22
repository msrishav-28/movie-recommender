"""
Watchlist Repository - Data access for Watchlist models.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from datetime import datetime
import logging

from app.db.models.watchlist import WatchlistItem

logger = logging.getLogger(__name__)


class WatchlistRepository:
    """Repository for Watchlist data access."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def add_item(self, item: WatchlistItem) -> WatchlistItem:
        """Add item to watchlist."""
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item
    
    async def get_item(self, user_id: str, movie_id: int) -> Optional[WatchlistItem]:
        """Get watchlist item."""
        result = await self.db.execute(
            select(WatchlistItem).where(
                WatchlistItem.user_id == user_id,
                WatchlistItem.movie_id == movie_id
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_watchlist(
        self,
        user_id: str,
        watched: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[WatchlistItem]:
        """Get user's watchlist."""
        stmt = select(WatchlistItem).where(WatchlistItem.user_id == user_id)
        
        if watched is not None:
            stmt = stmt.where(WatchlistItem.watched == watched)
        
        stmt = stmt.order_by(
            WatchlistItem.priority.desc().nullslast(),
            WatchlistItem.created_at.desc()
        ).offset(offset).limit(limit)
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def update_item(self, user_id: str, movie_id: int, data: dict) -> Optional[WatchlistItem]:
        """Update watchlist item."""
        result = await self.db.execute(
            select(WatchlistItem).where(
                WatchlistItem.user_id == user_id,
                WatchlistItem.movie_id == movie_id
            )
        )
        item = result.scalar_one_or_none()
        
        if item:
            for key, value in data.items():
                setattr(item, key, value)
            
            # Set watched_at if marking as watched
            if data.get('watched') and not item.watched_at:
                item.watched_at = datetime.utcnow()
            
            await self.db.commit()
            await self.db.refresh(item)
        
        return item
    
    async def remove_item(self, user_id: str, movie_id: int) -> bool:
        """Remove item from watchlist."""
        result = await self.db.execute(
            delete(WatchlistItem).where(
                WatchlistItem.user_id == user_id,
                WatchlistItem.movie_id == movie_id
            )
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def bulk_remove(self, user_id: str, movie_ids: List[int]) -> int:
        """Remove multiple items from watchlist."""
        result = await self.db.execute(
            delete(WatchlistItem).where(
                WatchlistItem.user_id == user_id,
                WatchlistItem.movie_id.in_(movie_ids)
            )
        )
        await self.db.commit()
        return result.rowcount
    
    async def mark_as_watched(self, user_id: str, movie_id: int) -> Optional[WatchlistItem]:
        """Mark watchlist item as watched."""
        return await self.update_item(
            user_id,
            movie_id,
            {"watched": True, "watched_at": datetime.utcnow()}
        )
    
    async def get_watchlist_stats(self, user_id: str) -> Dict[str, Any]:
        """Get watchlist statistics."""
        result = await self.db.execute(
            select(
                func.count(WatchlistItem.id).label('total'),
                func.count(WatchlistItem.id).filter(WatchlistItem.watched == True).label('watched'),
                func.count(WatchlistItem.id).filter(WatchlistItem.watched == False).label('unwatched'),
                func.avg(WatchlistItem.priority).label('avg_priority')
            ).where(WatchlistItem.user_id == user_id)
        )
        row = result.first()
        
        return {
            "total_items": row.total or 0,
            "watched_count": row.watched or 0,
            "unwatched_count": row.unwatched or 0,
            "avg_priority": float(row.avg_priority) if row.avg_priority else None
        }
    
    async def is_in_watchlist(self, user_id: str, movie_id: int) -> bool:
        """Check if movie is in user's watchlist."""
        result = await self.db.execute(
            select(WatchlistItem).where(
                WatchlistItem.user_id == user_id,
                WatchlistItem.movie_id == movie_id
            )
        )
        return result.scalar_one_or_none() is not None
    
    async def get_high_priority_items(self, user_id: str, limit: int = 10) -> List[WatchlistItem]:
        """Get high priority unwatched items."""
        result = await self.db.execute(
            select(WatchlistItem)
            .where(
                WatchlistItem.user_id == user_id,
                WatchlistItem.watched == False,
                WatchlistItem.priority.isnot(None)
            )
            .order_by(WatchlistItem.priority.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
