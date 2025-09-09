from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from models.user import User
from repositories.instagram_repository import instagram_repository
from auth.simple_auth import get_current_user

router = APIRouter()

class MediaInsight(BaseModel):
    metric: str
    value: int

class MediaPostDetail(BaseModel):
    ig_media_id: str
    ig_user_id: str
    timestamp: datetime
    media_type: str
    caption: Optional[str] = None
    media_url: str
    thumbnail_url: Optional[str] = None
    permalink: str

class MediaPostWithStats(BaseModel):
    ig_media_id: str
    ig_user_id: str
    timestamp: datetime
    media_type: str
    caption: Optional[str] = None
    media_url: str
    thumbnail_url: Optional[str] = None
    permalink: str
    like_count: int
    comments_count: int
    reach: Optional[int] = None
    views: Optional[int] = None
    shares: Optional[int] = None
    saved: Optional[int] = None

@router.get("/{account_id}", response_model=List[MediaPostDetail])
async def get_media_posts(
    account_id: str,
    limit: Optional[int] = Query(25, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """アカウントの投稿一覧を取得"""
    # Verify account exists
    account = await instagram_repository.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    # TODO: Implement actual media posts retrieval
    return []

@router.get("/{media_id}/insights", response_model=List[MediaInsight])
async def get_media_insights(
    media_id: str,
    current_user: User = Depends(get_current_user)
):
    """特定投稿のインサイトデータを取得"""
    # TODO: Implement actual insights retrieval
    return []

@router.get("/stats/{account_id}", response_model=List[MediaPostWithStats])
async def get_media_with_stats(
    account_id: str,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    media_type: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
):
    """統計データ付きの投稿一覧を取得（投稿分析ページ用）"""
    # Verify account exists
    account = await instagram_repository.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    # TODO: Implement actual media posts with stats retrieval
    return []