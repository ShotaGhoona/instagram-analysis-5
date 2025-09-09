from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime, date
from models.user import User
from repositories.instagram_repository import instagram_repository
from middleware.auth.simple_auth import get_current_user

router = APIRouter()

class PostAnalytics(BaseModel):
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
    engagement_rate: Optional[float] = None

class MonthlyStats(BaseModel):
    month: str
    followers_count: int
    follows_count: int
    media_count: int
    profile_views: int
    website_clicks: int
    total_likes: int
    total_comments: int
    total_shares: int
    total_saved: int

class YearlyAnalytics(BaseModel):
    account_id: str
    monthly_stats: List[MonthlyStats]
    total_posts: int
    avg_engagement_rate: float

class DailyStats(BaseModel):
    date: date
    posts_count: int
    new_followers: int
    reach: int
    profile_views: int
    website_clicks: int

class MonthlyAnalytics(BaseModel):
    account_id: str
    month: str
    daily_stats: List[DailyStats]

def calculate_engagement_rate(like_count: int, comments_count: int, shares: int, saved: int, reach: int) -> float:
    """Calculate engagement rate (small decimal 1 place)"""
    if reach == 0:
        return 0.0
    
    total_engagements = like_count + comments_count + shares + saved
    rate = (total_engagements / reach) * 100
    return round(rate, 1)

@router.get("/posts/{account_id}", response_model=List[PostAnalytics])
async def get_posts_analytics(
    account_id: str,
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    media_type: Optional[List[str]] = Query([], description="Filter by media types: IMAGE, VIDEO, CAROUSEL_ALBUM"),
    sort_by: str = Query('timestamp', description="Sort by field: timestamp, like_count, reach, engagement_rate"),
    sort_order: str = Query('desc', description="Sort order: asc, desc"),
    limit: int = Query(25, ge=1, le=100, description="Limit number of results"),
    current_user: User = Depends(get_current_user)
):
    """投稿分析データを取得（フィルタリング・ソート対応）"""
    # Verify account exists
    account = await instagram_repository.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    try:
        # Convert date to datetime for repository call
        start_datetime = datetime.combine(start_date, datetime.min.time()) if start_date else None
        end_datetime = datetime.combine(end_date, datetime.max.time()) if end_date else None
        
        # Get posts with stats from database
        posts_data = []
        
        # If multiple media types specified, get data for each type
        if media_type:
            for m_type in media_type:
                posts = await instagram_repository.get_media_posts_with_stats(
                    ig_user_id=account_id,
                    start_date=start_datetime,
                    end_date=end_datetime, 
                    media_type=m_type,
                    limit=limit
                )
                posts_data.extend(posts)
        else:
            # Get all posts without media type filter
            posts_data = await instagram_repository.get_media_posts_with_stats(
                ig_user_id=account_id,
                start_date=start_datetime,
                end_date=end_datetime,
                media_type=None,
                limit=limit
            )
        
        # Convert to response model with engagement rate calculation
        result = []
        for post in posts_data:
            # Calculate engagement rate
            engagement_rate = calculate_engagement_rate(
                like_count=post.get('like_count', 0),
                comments_count=post.get('comments_count', 0),
                shares=post.get('shares', 0),
                saved=post.get('saved', 0),
                reach=post.get('reach', 1)  # Avoid division by zero
            )
            
            # Parse timestamp string to datetime
            timestamp_str = post['timestamp']
            if isinstance(timestamp_str, str):
                # Handle ISO format timestamps
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            else:
                timestamp = timestamp_str
            
            post_analytics = PostAnalytics(
                ig_media_id=post['ig_media_id'],
                ig_user_id=post['ig_user_id'],
                timestamp=timestamp,
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
                saved=post.get('saved'),
                engagement_rate=engagement_rate
            )
            result.append(post_analytics)
        
        # Sort results if requested
        if sort_by and result:
            reverse_sort = (sort_order.lower() == 'desc')
            
            if sort_by == 'timestamp':
                result.sort(key=lambda x: x.timestamp, reverse=reverse_sort)
            elif sort_by == 'like_count':
                result.sort(key=lambda x: x.like_count, reverse=reverse_sort)
            elif sort_by == 'reach':
                result.sort(key=lambda x: x.reach or 0, reverse=reverse_sort)
            elif sort_by == 'engagement_rate':
                result.sort(key=lambda x: x.engagement_rate or 0, reverse=reverse_sort)
        
        # Apply limit after sorting (in case multiple media types were requested)
        return result[:limit]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch posts analytics: {str(e)}"
        )

@router.get("/yearly/{account_id}", response_model=YearlyAnalytics)
async def get_yearly_analytics(
    account_id: str,
    current_user: User = Depends(get_current_user)
):
    """年間分析データを取得"""
    # Verify account exists
    account = await instagram_repository.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    # TODO: Implement actual yearly analytics aggregation
    return YearlyAnalytics(
        account_id=account_id,
        monthly_stats=[],
        total_posts=0,
        avg_engagement_rate=0.0
    )

@router.get("/monthly/{account_id}", response_model=MonthlyAnalytics)
async def get_monthly_analytics(
    account_id: str,
    year: int = Query(...),
    month: int = Query(...),
    current_user: User = Depends(get_current_user)
):
    """月間分析データを取得"""
    # Verify account exists
    account = await instagram_repository.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    # TODO: Implement actual monthly analytics aggregation
    return MonthlyAnalytics(
        account_id=account_id,
        month=f"{year}-{month:02d}",
        daily_stats=[]
    )