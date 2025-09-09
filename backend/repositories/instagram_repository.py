from typing import Optional, List, Dict
from datetime import datetime
from models.instagram import InstagramAccount, MediaPost
from repositories.base import BaseRepository

class InstagramAccountRepository(BaseRepository[InstagramAccount]):
    """Instagram account data access repository"""
    
    def __init__(self):
        super().__init__("instagram_accounts")
    
    async def create(self, account: InstagramAccount) -> Optional[InstagramAccount]:
        """Create a new Instagram account"""
        try:
            result = self.client.table(self.table_name).insert({
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
    
    async def get_by_id(self, ig_user_id: str) -> Optional[InstagramAccount]:
        """Get Instagram account by ig_user_id"""
        try:
            result = self.client.table(self.table_name).select('*').eq('ig_user_id', ig_user_id).execute()
            return InstagramAccount(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error getting Instagram account: {e}")
            return None
    
    async def get_all(self) -> List[InstagramAccount]:
        """Get all Instagram accounts"""
        try:
            result = self.client.table(self.table_name).select('*').execute()
            return [InstagramAccount(**account) for account in result.data]
        except Exception as e:
            print(f"Error getting Instagram accounts: {e}")
            return []
    
    async def update(self, ig_user_id: str, update_data: dict) -> Optional[InstagramAccount]:
        """Update Instagram account by ig_user_id"""
        try:
            result = self.client.table(self.table_name).update(update_data).eq('ig_user_id', ig_user_id).execute()
            return InstagramAccount(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error updating Instagram account: {e}")
            return None
    
    async def update_token(self, ig_user_id: str, access_token: str) -> bool:
        """Update access token for Instagram account"""
        try:
            result = self.client.table(self.table_name).update({
                'access_token': access_token
            }).eq('ig_user_id', ig_user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error updating Instagram account token: {e}")
            return False
    
    async def delete(self, ig_user_id: str) -> bool:
        """Delete Instagram account by ig_user_id"""
        try:
            result = self.client.table(self.table_name).delete().eq('ig_user_id', ig_user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error deleting Instagram account: {e}")
            return False
    
    async def upsert_account(self, account_data: dict) -> Optional[InstagramAccount]:
        """Insert new account or update existing account"""
        try:
            # Try to get existing account
            existing = await self.get_by_id(account_data['ig_user_id'])
            
            if existing:
                # Update existing account
                update_data = {
                    'name': account_data['page_name'],
                    'access_token': account_data['access_token'],
                    'username': account_data['username'],
                    'profile_picture_url': account_data.get('profile_picture_url')
                }
                return await self.update(account_data['ig_user_id'], update_data)
            else:
                # Create new account
                new_account = InstagramAccount(
                    name=account_data['page_name'],
                    ig_user_id=account_data['ig_user_id'],
                    access_token=account_data['access_token'],
                    username=account_data['username'],
                    profile_picture_url=account_data.get('profile_picture_url')
                )
                return await self.create(new_account)
        except Exception as e:
            print(f"Error upserting Instagram account: {e}")
            return None
    
    async def save_media_posts(self, media_posts: List[Dict]) -> int:
        """Save media posts to database (UPSERT)"""
        try:
            saved_count = 0
            for media_data in media_posts:
                # Check if media already exists
                existing = self.client.table('media_posts').select('id').eq('ig_media_id', media_data['id']).execute()
                
                post_data = {
                    'ig_media_id': media_data['id'],
                    'ig_user_id': media_data.get('ig_user_id', ''),  # Will be set by caller
                    'timestamp': media_data['timestamp'],
                    'media_type': media_data['media_type'],
                    'caption': media_data.get('caption'),
                    'media_url': media_data['media_url'],
                    'thumbnail_url': media_data.get('thumbnail_url'),
                    'permalink': media_data['permalink']
                }
                
                if existing.data:
                    # Update existing post
                    self.client.table('media_posts').update(post_data).eq('ig_media_id', media_data['id']).execute()
                else:
                    # Insert new post
                    self.client.table('media_posts').insert(post_data).execute()
                
                saved_count += 1
            
            return saved_count
        except Exception as e:
            print(f"Error saving media posts: {e}")
            return 0
    
    async def get_media_posts(self, ig_user_id: str, limit: int = 25) -> List[Dict]:
        """Get media posts from database"""
        try:
            result = self.client.table('media_posts').select('*').eq('ig_user_id', ig_user_id).order('timestamp', desc=True).limit(limit).execute()
            return result.data
        except Exception as e:
            print(f"Error getting media posts: {e}")
            return []
    
    async def get_media_posts_with_stats(self, ig_user_id: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, media_type: Optional[str] = None, limit: int = 25) -> List[Dict]:
        """Get media posts with latest stats for posts analysis page"""
        try:
            query = self.client.table('media_posts').select('''
                *,
                daily_media_stats(date, like_count, comments_count, reach, views, shares, saved)
            ''').eq('ig_user_id', ig_user_id)
            
            if media_type:
                query = query.eq('media_type', media_type)
            if start_date:
                query = query.gte('timestamp', start_date.isoformat())
            if end_date:
                query = query.lte('timestamp', end_date.isoformat())
                
            result = query.order('timestamp', desc=True).limit(limit).execute()
            
            # Process data to get latest stats for each post
            processed_data = []
            for post in result.data:
                # Get latest stats if available
                latest_stats = None
                if post.get('daily_media_stats'):
                    # Sort by date and get latest
                    stats_sorted = sorted(post['daily_media_stats'], key=lambda x: x['date'], reverse=True)
                    if stats_sorted:
                        latest_stats = stats_sorted[0]
                
                post_with_stats = {
                    **post,
                    'like_count': latest_stats['like_count'] if latest_stats else 0,
                    'comments_count': latest_stats['comments_count'] if latest_stats else 0,
                    'reach': latest_stats.get('reach') if latest_stats else None,
                    'views': latest_stats.get('views') if latest_stats else None,
                    'shares': latest_stats.get('shares') if latest_stats else None,
                    'saved': latest_stats.get('saved') if latest_stats else None
                }
                del post_with_stats['daily_media_stats']  # Clean up
                processed_data.append(post_with_stats)
            
            return processed_data
            
        except Exception as e:
            print(f"Error getting media posts with stats: {e}")
            return []

# Repository instance
instagram_repository = InstagramAccountRepository()