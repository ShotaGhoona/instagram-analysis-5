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
    
    # Get media posts from database
    media_posts = await instagram_repository.get_media_posts(account_id, limit)
    
    # Convert to response model
    result = []
    for post in media_posts:
        result.append(MediaPostDetail(
            ig_media_id=post['ig_media_id'],
            ig_user_id=post['ig_user_id'],
            timestamp=datetime.fromisoformat(post['timestamp'].replace('Z', '+00:00')),
            media_type=post['media_type'],
            caption=post.get('caption'),
            media_url=post['media_url'],
            thumbnail_url=post.get('thumbnail_url'),
            permalink=post['permalink']
        ))
    
    return result

@router.get("/{media_id}/insights", response_model=List[MediaInsight])
async def get_media_insights(
    media_id: str,
    current_user: User = Depends(get_current_user)
):
    """特定投稿のインサイトデータを取得"""
    # TODO: B0204 インサイトデータ取得後に実装
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
    
    # Get media posts with stats from database
    media_posts = await instagram_repository.get_media_posts_with_stats(
        account_id, start_date, end_date, media_type
    )
    
    # Convert to response model
    result = []
    for post in media_posts:
        result.append(MediaPostWithStats(
            ig_media_id=post['ig_media_id'],
            ig_user_id=post['ig_user_id'],
            timestamp=datetime.fromisoformat(post['timestamp'].replace('Z', '+00:00')),
            media_type=post['media_type'],
            caption=post.get('caption'),
            media_url=post['media_url'],
            thumbnail_url=post.get('thumbnail_url'),
            permalink=post['permalink'],
            like_count=post.get('like_count', 0),
            comments_count=post.get('comments_count', 0),
            reach=post.get('reach'),
            views=post.get('views'),
            shares=post.get('shares'),
            saved=post.get('saved')
        ))
    
    return result