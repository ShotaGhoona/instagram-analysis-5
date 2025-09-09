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
    # Get latest stats from database
    media_stats = await instagram_repository.get_media_stats(media_id)
    
    if not media_stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media insights not found"
        )
    
    # Get latest stats (most recent entry)
    latest_stats = media_stats[0]
    
    # Convert to response model
    insights = []
    
    # Add available metrics
    if latest_stats.get('reach') is not None:
        insights.append(MediaInsight(metric="reach", value=latest_stats['reach']))
    if latest_stats.get('views') is not None:
        insights.append(MediaInsight(metric="views", value=latest_stats['views']))
    if latest_stats.get('shares') is not None:
        insights.append(MediaInsight(metric="shares", value=latest_stats['shares']))
    if latest_stats.get('saved') is not None:
        insights.append(MediaInsight(metric="saved", value=latest_stats['saved']))
    
    return insights

@router.post("/{media_id}/collect-insights")
async def collect_media_insights(
    media_id: str,
    current_user: User = Depends(get_current_user)
):
    """特定投稿のインサイトデータをInstagram APIから収集"""
    # Get media post info first
    media_posts = await instagram_repository.get_media_posts("", 100)  # Get all posts
    target_media = None
    
    for post in media_posts:
        if post['ig_media_id'] == media_id:
            target_media = post
            break
    
    if not target_media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media post not found"
        )
    
    # Get account info for access token
    account = await instagram_repository.get_by_id(target_media['ig_user_id'])
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    # Collect insights using service
    from services.instagram_service import instagram_service
    result = await instagram_service.collect_media_insights(
        media_id,
        target_media['media_type'],
        account.access_token,
        target_media.get('like_count', 0),
        target_media.get('comments_count', 0)
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to collect insights: {result.get('error', 'Unknown error')}"
        )
    
    return {
        "success": True,
        "message": "Insights collected successfully",
        "collected_metrics": result.get("collected_metrics", 0),
        "total_metrics": result.get("total_metrics", 0)
    }

@router.post("/collect-all-insights/{account_id}")
async def collect_all_media_insights(
    account_id: str,
    limit: Optional[int] = Query(10, ge=1, le=25),
    current_user: User = Depends(get_current_user)
):
    """アカウントの全投稿のインサイトデータを収集"""
    # Verify account exists
    account = await instagram_repository.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    # Collect all media insights using service
    from services.instagram_service import instagram_service
    result = await instagram_service.collect_all_media_insights(
        account_id,
        account.access_token,
        limit
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to collect insights: {result.get('error', 'Unknown error')}"
        )
    
    return {
        "success": True,
        "message": "All insights collected successfully",
        "processed_media": result.get("processed_media", 0),
        "successful_media": result.get("successful_media", 0)
    }

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