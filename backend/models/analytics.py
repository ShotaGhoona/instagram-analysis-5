from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class YearlyAnalyticsResponse(BaseModel):
    """Yearly analytics response model"""
    account_id: str
    year: int
    monthly_data: List[dict]
    summary: dict

class MonthlyAnalyticsResponse(BaseModel):
    """Monthly analytics response model"""
    account_id: str
    year: int
    month: int
    daily_data: List[dict]
    summary: dict

class PostsAnalyticsResponse(BaseModel):
    """Posts analytics response model"""
    account_id: str
    posts: List[dict]
    summary: dict
    filters: dict