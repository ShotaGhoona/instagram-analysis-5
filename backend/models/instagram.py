from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class InstagramAccount(BaseModel):
    """Instagram account data model"""
    id: Optional[int] = None
    name: str
    ig_user_id: str
    access_token: str
    username: str
    profile_picture_url: Optional[str] = None
    created_at: Optional[datetime] = None

class DailyAccountStats(BaseModel):
    """Daily account statistics model"""
    id: Optional[int] = None
    date: datetime
    ig_user_id: str
    followers_count: int
    follows_count: int
    media_count: int
    profile_views: Optional[int] = None
    website_clicks: Optional[int] = None

class MediaPost(BaseModel):
    """Media post data model"""
    id: Optional[int] = None
    ig_media_id: str
    ig_user_id: str
    timestamp: datetime
    media_type: str  # IMAGE, VIDEO, CAROUSEL_ALBUM
    caption: Optional[str] = None
    media_url: str
    thumbnail_url: Optional[str] = None
    permalink: str

class DailyMediaStats(BaseModel):
    """Daily media statistics model"""
    id: Optional[int] = None
    date: datetime
    ig_media_id: str
    like_count: int
    comments_count: int
    reach: Optional[int] = None
    views: Optional[int] = None
    shares: Optional[int] = None
    saved: Optional[int] = None

# Request/Response models
class TokenRefreshRequest(BaseModel):
    """Token refresh request model"""
    app_id: str
    app_secret: str
    access_token: str

class TokenRefreshResponse(BaseModel):
    """Token refresh response model"""
    success: bool
    message: str
    updated_accounts: int
    new_accounts: int
    total_processed: int
    errors: list = []