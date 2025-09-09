from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from utils.supabase_client import supabase_client

class User(BaseModel):
    id: Optional[int] = None
    username: str
    password_hash: str
    created_at: Optional[datetime] = None

class InstagramAccount(BaseModel):
    id: Optional[int] = None
    name: str
    ig_user_id: str
    access_token: str
    username: str
    profile_picture_url: Optional[str] = None
    created_at: Optional[datetime] = None

class DailyAccountStats(BaseModel):
    id: Optional[int] = None
    date: datetime
    ig_user_id: str
    followers_count: int
    follows_count: int
    media_count: int
    profile_views: Optional[int] = None
    website_clicks: Optional[int] = None

class MediaPost(BaseModel):
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
    id: Optional[int] = None
    date: datetime
    ig_media_id: str
    like_count: int
    comments_count: int
    reach: Optional[int] = None
    views: Optional[int] = None
    shares: Optional[int] = None
    saved: Optional[int] = None

class DatabaseManager:
    def __init__(self):
        self.client = supabase_client.client
    
    async def create_tables(self):
        """Create all necessary tables in Supabase"""
        tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS instagram_accounts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                ig_user_id VARCHAR(50) UNIQUE NOT NULL,
                access_token TEXT NOT NULL,
                username VARCHAR(100) NOT NULL,
                profile_picture_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS daily_account_stats (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                ig_user_id VARCHAR(50) NOT NULL,
                followers_count INTEGER NOT NULL,
                follows_count INTEGER NOT NULL,
                media_count INTEGER NOT NULL,
                profile_views INTEGER,
                website_clicks INTEGER,
                UNIQUE(date, ig_user_id),
                FOREIGN KEY (ig_user_id) REFERENCES instagram_accounts(ig_user_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS media_posts (
                id SERIAL PRIMARY KEY,
                ig_media_id VARCHAR(50) UNIQUE NOT NULL,
                ig_user_id VARCHAR(50) NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                media_type VARCHAR(20) NOT NULL,
                caption TEXT,
                media_url TEXT NOT NULL,
                thumbnail_url TEXT,
                permalink TEXT NOT NULL,
                FOREIGN KEY (ig_user_id) REFERENCES instagram_accounts(ig_user_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS daily_media_stats (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                ig_media_id VARCHAR(50) NOT NULL,
                like_count INTEGER NOT NULL,
                comments_count INTEGER NOT NULL,
                reach INTEGER,
                views INTEGER,
                shares INTEGER,
                saved INTEGER,
                UNIQUE(date, ig_media_id),
                FOREIGN KEY (ig_media_id) REFERENCES media_posts(ig_media_id)
            );
            """
        ]
        
        try:
            for sql in tables_sql:
                result = self.client.rpc('exec_sql', {'sql': sql}).execute()
            print("✅ Database tables created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    # User operations
    async def create_user(self, user: User) -> Optional[User]:
        try:
            result = self.client.table('users').insert({
                'username': user.username,
                'password_hash': user.password_hash
            }).execute()
            return User(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        try:
            result = self.client.table('users').select('*').eq('username', username).execute()
            return User(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    # Instagram Account operations
    async def create_instagram_account(self, account: InstagramAccount) -> Optional[InstagramAccount]:
        try:
            result = self.client.table('instagram_accounts').insert({
                'name': account.name,
                'ig_user_id': account.ig_user_id,
                'access_token': account.access_token,
                'username': account.username,
                'profile_picture_url': account.profile_picture_url
            }).execute()
            return InstagramAccount(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error creating Instagram account: {e}")
            return None
    
    async def get_instagram_accounts(self) -> List[InstagramAccount]:
        try:
            result = self.client.table('instagram_accounts').select('*').execute()
            return [InstagramAccount(**account) for account in result.data]
        except Exception as e:
            print(f"Error getting Instagram accounts: {e}")
            return []
    
    async def get_instagram_account(self, ig_user_id: str) -> Optional[InstagramAccount]:
        try:
            result = self.client.table('instagram_accounts').select('*').eq('ig_user_id', ig_user_id).execute()
            return InstagramAccount(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error getting Instagram account: {e}")
            return None
    
    async def update_instagram_account_token(self, ig_user_id: str, access_token: str) -> bool:
        """Update access token for existing Instagram account"""
        try:
            result = self.client.table('instagram_accounts').update({
                'access_token': access_token
            }).eq('ig_user_id', ig_user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error updating Instagram account token: {e}")
            return False
    
    async def upsert_instagram_account(self, account_data: dict) -> Optional[InstagramAccount]:
        """Insert new account or update existing account"""
        try:
            # Try to get existing account
            existing = await self.get_instagram_account(account_data['ig_user_id'])
            
            if existing:
                # Update existing account
                result = self.client.table('instagram_accounts').update({
                    'name': account_data['page_name'],
                    'access_token': account_data['access_token'],
                    'username': account_data['username'],
                    'profile_picture_url': account_data.get('profile_picture_url')
                }).eq('ig_user_id', account_data['ig_user_id']).execute()
                return InstagramAccount(**result.data[0]) if result.data else None
            else:
                # Create new account
                new_account = InstagramAccount(
                    name=account_data['page_name'],
                    ig_user_id=account_data['ig_user_id'],
                    access_token=account_data['access_token'],
                    username=account_data['username'],
                    profile_picture_url=account_data.get('profile_picture_url')
                )
                return await self.create_instagram_account(new_account)
        except Exception as e:
            print(f"Error upserting Instagram account: {e}")
            return None

db_manager = DatabaseManager()