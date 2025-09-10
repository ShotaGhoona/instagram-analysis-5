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
    year: Optional[int] = Query(None, description="対象年（未指定時は現在年）"),
    current_user: User = Depends(get_current_user)
):
    """年間分析データを取得"""
    # Set default year if not provided
    if year is None:
        year = datetime.now().year
    
    # Validate year parameter
    if not isinstance(year, int):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="年は整数で指定してください"
        )
    if year < 2020 or year > 2030:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="年は2020年から2030年の範囲で指定してください"
        )
    
    # Verify account exists
    account = await instagram_repository.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    try:
        # Get monthly account stats and media aggregation
        account_stats = await instagram_repository.get_monthly_account_stats(account_id, year)
        media_stats = await instagram_repository.get_monthly_media_aggregation(account_id, year)
        total_posts = await instagram_repository.get_total_posts_count(account_id, year)
        
        # Merge data by month and calculate metrics
        monthly_data = {}
        
        # Process account stats
        for stat in account_stats:
            month = stat['month']
            monthly_data[month] = {
                'month': month,
                'followers_count': stat['followers_count'],
                'follows_count': 0,  # Will be calculated as difference
                'media_count': 0,
                'profile_views': stat['profile_views'],
                'website_clicks': stat['website_clicks'],
                'total_likes': 0,
                'total_comments': 0,
                'total_shares': 0,
                'total_saved': 0
            }
        
        # Process media stats
        for stat in media_stats:
            month = stat['month']
            if month in monthly_data:
                monthly_data[month].update({
                    'media_count': stat['media_count'],
                    'total_likes': stat['total_likes'],
                    'total_comments': stat['total_comments'],
                    'total_shares': stat['total_shares'],
                    'total_saved': stat['total_saved']
                })
            else:
                monthly_data[month] = {
                    'month': month,
                    'followers_count': 0,
                    'follows_count': 0,
                    'media_count': stat['media_count'],
                    'profile_views': 0,
                    'website_clicks': 0,
                    'total_likes': stat['total_likes'],
                    'total_comments': stat['total_comments'],
                    'total_shares': stat['total_shares'],
                    'total_saved': stat['total_saved']
                }
        
        # Sort by month and calculate follows_count (new followers)
        sorted_months = sorted(monthly_data.keys())
        monthly_stats = []
        prev_followers = 0
        
        for month in sorted_months:
            month_data = monthly_data[month]
            current_followers = month_data['followers_count']
            
            # Calculate new followers as difference from previous month
            if prev_followers > 0:
                month_data['follows_count'] = current_followers - prev_followers
            else:
                month_data['follows_count'] = current_followers
            
            monthly_stats.append(MonthlyStats(**month_data))
            prev_followers = current_followers
        
        # Handle empty data case
        if not monthly_stats:
            return YearlyAnalytics(
                account_id=account_id,
                monthly_stats=[],
                total_posts=0,
                avg_engagement_rate=0.0
            )
        
        # Calculate average engagement rate
        total_engagements = sum(stat.total_likes + stat.total_comments + stat.total_shares + stat.total_saved for stat in monthly_stats)
        avg_engagement_rate = 0.0
        if total_posts > 0:
            # Simple approximation for avg engagement rate
            avg_engagement_rate = round((total_engagements / total_posts) * 0.1, 1)  # Rough estimation
        
        return YearlyAnalytics(
            account_id=account_id,
            monthly_stats=monthly_stats,
            total_posts=total_posts,
            avg_engagement_rate=avg_engagement_rate
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch yearly analytics: {str(e)}"
        )

@router.get("/monthly/{account_id}", response_model=MonthlyAnalytics)
async def get_monthly_analytics(
    account_id: str,
    year: Optional[int] = Query(None, description="対象年（未指定時は現在年）"),
    month: Optional[int] = Query(None, ge=1, le=12, description="対象月（未指定時は現在月）"),
    current_user: User = Depends(get_current_user)
):
    """月間分析データを取得"""
    # Set default year and month if not provided
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    
    # Validate year parameter
    if not isinstance(year, int):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="年は整数で指定してください"
        )
    if year < 2020 or year > 2030:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="年は2020年から2030年の範囲で指定してください"
        )
    
    # Validate month parameter
    if not isinstance(month, int):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="月は整数で指定してください"
        )
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="月は1から12の範囲で指定してください"
        )
    
    # Verify account exists
    account = await instagram_repository.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    try:
        # Get daily account stats and media aggregation
        account_stats = await instagram_repository.get_daily_account_stats(account_id, year, month)
        media_stats = await instagram_repository.get_daily_media_stats_aggregation(account_id, year, month)
        
        # Merge account and media data by date
        daily_data = {}
        
        # Process account stats (includes profile_views, website_clicks, new_followers)
        for stat in account_stats:
            date = stat['date']
            daily_data[date] = {
                'date': date,
                'posts_count': stat.get('posts_count', 0),
                'new_followers': stat.get('new_followers', 0),
                'reach': stat.get('reach', 0),
                'profile_views': stat.get('profile_views', 0),
                'website_clicks': stat.get('website_clicks', 0)
            }
        
        # Process media stats (includes posts_count, reach)
        for stat in media_stats:
            date = stat['date']
            if date in daily_data:
                # Update posts_count and reach from media data
                daily_data[date]['posts_count'] = stat.get('posts_count', 0)
                daily_data[date]['reach'] = stat.get('reach', 0)
            else:
                # Create new entry if not exists
                daily_data[date] = {
                    'date': date,
                    'posts_count': stat.get('posts_count', 0),
                    'new_followers': 0,
                    'reach': stat.get('reach', 0),
                    'profile_views': 0,
                    'website_clicks': 0
                }
        
        # Sort by date and convert to DailyStats
        sorted_dates = sorted(daily_data.keys())
        daily_stats = []
        
        for date in sorted_dates:
            day_data = daily_data[date]
            daily_stats.append(DailyStats(
                date=day_data['date'],
                posts_count=day_data['posts_count'],
                new_followers=day_data['new_followers'],
                reach=day_data['reach'],
                profile_views=day_data['profile_views'],
                website_clicks=day_data['website_clicks']
            ))
        
        # Handle empty data case - return empty daily_stats instead of error
        return MonthlyAnalytics(
            account_id=account_id,
            month=f"{year}-{month:02d}",
            daily_stats=daily_stats
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch monthly analytics: {str(e)}"
        )