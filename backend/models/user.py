from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    """User data model"""
    id: Optional[int] = None
    username: str
    password_hash: str
    created_at: Optional[datetime] = None

class UserCreate(BaseModel):
    """User creation model"""
    username: str
    password: str

class UserLogin(BaseModel):
    """User login model"""
    username: str
    password: str