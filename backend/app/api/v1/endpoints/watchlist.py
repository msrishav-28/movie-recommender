"""Watchlist and lists endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.db.database import get_db
from app.db.models.watchlist import WatchlistItem, UserList, ListItem
from app.db.models.user import User
from app.api.deps import get_current_active_user

router = APIRouter()


class AddToWatchlistRequest(BaseModel):
    movie_id: int
    priority: int = Field(5, ge=1, le=10)
    notes: Optional[str] = None
    tags: List[str] = []


class WatchlistItemResponse(BaseModel):
    id: int
    movie_id: int
    priority: int
    is_watched: bool
    notes: Optional[str]
    tags: List[str]
    added_at: datetime
    
    class Config:
        from_attributes = True


class CreateListRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    is_public: bool = True


class ListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_public: bool
    likes_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/", response_model=WatchlistItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_watchlist(
    data: AddToWatchlistRequest,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add movie to watchlist.
    
    - **movie_id**: Movie to add
    - **priority**: 1-10 (10 = highest priority)
    - **notes**: Optional personal notes
    - **tags**: Custom tags for organization
    """
    
    # Check if already in watchlist
    result = await db.execute(
        select(WatchlistItem).where(
            WatchlistItem.user_id == user.id,
            WatchlistItem.movie_id == data.movie_id
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Movie already in watchlist"
        )
    
    # Create watchlist item
    item = WatchlistItem(
        user_id=user.id,
        movie_id=data.movie_id,
        priority=data.priority,
        notes=data.notes,
        tags=data.tags
    )
    
    db.add(item)
    await db.commit()
    await db.refresh(item)
    
    return item


@router.get("/", response_model=List[WatchlistItemResponse])
async def get_my_watchlist(
    watched: Optional[bool] = Query(None),
    sort_by: str = Query("priority", regex="^(priority|added_at)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's watchlist.
    
    - **watched**: Filter by watched status (null = all)
    - **sort_by**: Sort by priority or added_at
    - **page**: Page number
    - **page_size**: Items per page
    """
    
    query = select(WatchlistItem).where(WatchlistItem.user_id == user.id)
    
    if watched is not None:
        query = query.where(WatchlistItem.is_watched == watched)
    
    if sort_by == "priority":
        query = query.order_by(WatchlistItem.priority.desc())
    else:
        query = query.order_by(WatchlistItem.added_at.desc())
    
    offset = (page - 1) * page_size
    result = await db.execute(query.offset(offset).limit(page_size))
    items = result.scalars().all()
    
    return [WatchlistItemResponse.from_orm(item) for item in items]


@router.put("/{item_id}")
async def update_watchlist_item(
    item_id: int,
    priority: Optional[int] = Field(None, ge=1, le=10),
    is_watched: Optional[bool] = None,
    notes: Optional[str] = None,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update watchlist item."""
    
    result = await db.execute(
        select(WatchlistItem).where(
            WatchlistItem.id == item_id,
            WatchlistItem.user_id == user.id
        )
    )
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found"
        )
    
    if priority is not None:
        item.priority = priority
    if is_watched is not None:
        item.is_watched = is_watched
        if is_watched:
            item.watched_at = datetime.utcnow()
    if notes is not None:
        item.notes = notes
    
    await db.commit()
    await db.refresh(item)
    
    return WatchlistItemResponse.from_orm(item)


@router.delete("/{item_id}")
async def remove_from_watchlist(
    item_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove movie from watchlist."""
    
    result = await db.execute(
        select(WatchlistItem).where(
            WatchlistItem.id == item_id,
            WatchlistItem.user_id == user.id
        )
    )
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found"
        )
    
    await db.delete(item)
    await db.commit()
    
    return {"status": "removed"}


# Custom Lists

@router.post("/lists", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
async def create_list(
    data: CreateListRequest,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a custom list.
    
    - **name**: List name (required)
    - **description**: Optional description
    - **is_public**: Public or private
    """
    
    user_list = UserList(
        user_id=user.id,
        name=data.name,
        description=data.description,
        is_public=data.is_public
    )
    
    db.add(user_list)
    await db.commit()
    await db.refresh(user_list)
    
    return user_list


@router.get("/lists", response_model=List[ListResponse])
async def get_my_lists(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's lists."""
    
    result = await db.execute(
        select(UserList)
        .where(UserList.user_id == user.id)
        .order_by(UserList.created_at.desc())
    )
    lists = result.scalars().all()
    
    return [ListResponse.from_orm(lst) for lst in lists]


@router.post("/lists/{list_id}/items")
async def add_to_list(
    list_id: int,
    movie_id: int,
    notes: Optional[str] = None,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Add movie to a list."""
    
    # Verify list belongs to user
    result = await db.execute(
        select(UserList).where(
            UserList.id == list_id,
            UserList.user_id == user.id
        )
    )
    user_list = result.scalar_one_or_none()
    
    if not user_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )
    
    # Check if movie already in list
    result = await db.execute(
        select(ListItem).where(
            ListItem.list_id == list_id,
            ListItem.movie_id == movie_id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Movie already in list"
        )
    
    # Get next position
    result = await db.execute(
        select(ListItem)
        .where(ListItem.list_id == list_id)
        .order_by(ListItem.position.desc())
    )
    last_item = result.scalars().first()
    next_position = (last_item.position + 1) if last_item else 1
    
    # Add to list
    item = ListItem(
        list_id=list_id,
        movie_id=movie_id,
        position=next_position,
        notes=notes,
        added_by=user.id
    )
    
    db.add(item)
    await db.commit()
    
    return {"status": "added", "position": next_position}
