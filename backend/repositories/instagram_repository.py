from typing import Optional, List, Dict
from datetime import datetime
from models.instagram import InstagramAccount, MediaPost
from repositories.base import BaseRepository
from core.exceptions import DatabaseConnectionError

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
            self._log_database_error("create", e)
            return None
    
    async def get_by_id(self, ig_user_id: str) -> Optional[InstagramAccount]:
        """Get Instagram account by ig_user_id"""
        try:
            result = self.client.table(self.table_name).select('*').eq('ig_user_id', ig_user_id).execute()
            return InstagramAccount(**result.data[0]) if result.data else None
        except Exception as e:
            self._log_database_error("get_by_id", e)
            return None
    
    async def get_all(self) -> List[InstagramAccount]:
        """Get all Instagram accounts"""
        try:
            result = self.client.table(self.table_name).select('*').execute()
            return [InstagramAccount(**account) for account in result.data]
        except Exception as e:
            self._log_database_error("get_all", e)
            return []
    
    async def update(self, ig_user_id: str, update_data: dict) -> Optional[InstagramAccount]:
        """Update Instagram account by ig_user_id"""
        try:
            result = self.client.table(self.table_name).update(update_data).eq('ig_user_id', ig_user_id).execute()
            return InstagramAccount(**result.data[0]) if result.data else None
        except Exception as e:
            self._log_database_error("update", e)
            return None
    
    def _log_database_error(self, operation: str, error: Exception):
        """Log database error in structured format"""
        error_type = type(error).__name__
        print(f"❌ Database Error: {operation}")
        print(f"   🔧 Operation: {operation}")
        print(f"   ⚠️ Type: {error_type}")
        print(f"   💬 Message: {str(error)}")
        
        # Classify common Supabase errors
        error_str = str(error).lower()
        if "connection" in error_str or "network" in error_str:
            print(f"   📊 Classification: CONNECTION_ERROR")
        elif "unique" in error_str or "duplicate" in error_str:
            print(f"   📊 Classification: DUPLICATE_KEY_ERROR")
        elif "auth" in error_str or "permission" in error_str:
            print(f"   📊 Classification: PERMISSION_ERROR")
        else:
            print(f"   📊 Classification: UNKNOWN_DATABASE_ERROR")
    
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
    
    async def save_daily_media_stats(self, media_stats: List[Dict]) -> int:
        """Save daily media statistics to database (UPSERT)"""
        try:
            saved_count = 0
            today = datetime.now().date().isoformat()
            
            for stats_data in media_stats:
                # Check if stats already exist for today
                existing = self.client.table('daily_media_stats').select('id').eq('ig_media_id', stats_data['ig_media_id']).eq('date', today).execute()
                
                stats_record = {
                    'date': today,
                    'ig_media_id': stats_data['ig_media_id'],
                    'like_count': stats_data.get('like_count', 0),
                    'comments_count': stats_data.get('comments_count', 0),
                    'reach': stats_data.get('reach'),
                    'views': stats_data.get('views'),
                    'shares': stats_data.get('shares'),
                    'saved': stats_data.get('saved')
                }
                
                if existing.data:
                    # Update existing stats
                    self.client.table('daily_media_stats').update(stats_record).eq('ig_media_id', stats_data['ig_media_id']).eq('date', today).execute()
                else:
                    # Insert new stats
                    self.client.table('daily_media_stats').insert(stats_record).execute()
                
                saved_count += 1
            
            return saved_count
        except Exception as e:
            print(f"Error saving daily media stats: {e}")
            return 0
    
    async def get_media_stats(self, ig_media_id: str, date_range: Optional[tuple] = None) -> List[Dict]:
        """Get media statistics from database"""
        try:
            query = self.client.table('daily_media_stats').select('*').eq('ig_media_id', ig_media_id)
            
            if date_range:
                start_date, end_date = date_range
                query = query.gte('date', start_date.isoformat()).lte('date', end_date.isoformat())
            
            result = query.order('date', desc=True).execute()
            return result.data
        except Exception as e:
            print(f"Error getting media stats: {e}")
            return []
    
    async def get_latest_media_stats(self, ig_media_ids: List[str]) -> Dict[str, Dict]:
        """Get latest stats for multiple media posts"""
        try:
            latest_stats = {}
            
            for ig_media_id in ig_media_ids:
                result = self.client.table('daily_media_stats').select('*').eq('ig_media_id', ig_media_id).order('date', desc=True).limit(1).execute()
                
                if result.data:
                    latest_stats[ig_media_id] = result.data[0]
                else:
                    # Default empty stats
                    latest_stats[ig_media_id] = {
                        'like_count': 0,
                        'comments_count': 0,
                        'reach': None,
                        'views': None,
                        'shares': None,
                        'saved': None
                    }
            
            return latest_stats
        except Exception as e:
            print(f"Error getting latest media stats: {e}")
            return {}
    
    async def save_daily_account_insights(self, account_insights: List[Dict]) -> int:
        """Save daily account insights to daily_account_stats table"""
        try:
            saved_count = 0
            today = datetime.now().date().isoformat()
            
            for insights_data in account_insights:
                ig_user_id = insights_data['ig_user_id']
                
                # Check if account stats already exist for today
                existing = self.client.table('daily_account_stats').select('id').eq('ig_user_id', ig_user_id).eq('date', today).execute()
                
                # Prepare account stats record with default values for required fields
                stats_record = {
                    'date': today,
                    'ig_user_id': ig_user_id,
                    'followers_count': insights_data.get('followers_count', 0),  # Default to 0
                    'follows_count': insights_data.get('follows_count', 0),      # Default to 0
                    'media_count': insights_data.get('media_count', 0),          # Default to 0
                    'profile_views': insights_data.get('profile_views'),
                    'website_clicks': insights_data.get('website_clicks')
                }
                
                if existing.data:
                    # Update existing account stats (only update provided fields)
                    update_data = {}
                    if 'profile_views' in insights_data:
                        update_data['profile_views'] = insights_data['profile_views']
                    if 'website_clicks' in insights_data:
                        update_data['website_clicks'] = insights_data['website_clicks']
                    
                    if update_data:  # Only update if there's data to update
                        self.client.table('daily_account_stats').update(update_data).eq('ig_user_id', ig_user_id).eq('date', today).execute()
                else:
                    # Insert new account stats
                    self.client.table('daily_account_stats').insert(stats_record).execute()
                
                saved_count += 1
            
            return saved_count
        except Exception as e:
            print(f"Error saving daily account insights: {e}")
            return 0
    
    async def get_monthly_account_stats(self, ig_user_id: str, year: Optional[int] = None) -> List[Dict]:
        """Get monthly aggregated account statistics"""
        try:
            # Use Supabase table query with date operations
            query = self.client.table('daily_account_stats').select('*').eq('ig_user_id', ig_user_id)
            
            if year:
                start_date = f"{year}-01-01"
                end_date = f"{year}-12-31"
                query = query.gte('date', start_date).lte('date', end_date)
            
            result = query.execute()
            
            # Group by month manually
            monthly_data = {}
            for row in result.data:
                date_str = row['date']
                month = date_str[:7]  # "2023-04"
                
                if month not in monthly_data:
                    monthly_data[month] = {
                        'month': month,
                        'followers_count': 0,
                        'profile_views': 0,
                        'website_clicks': 0,
                        '_count': 0
                    }
                
                monthly_data[month]['followers_count'] += row.get('followers_count', 0)
                monthly_data[month]['profile_views'] += row.get('profile_views', 0)
                monthly_data[month]['website_clicks'] += row.get('website_clicks', 0)
                monthly_data[month]['_count'] += 1
            
            # Calculate averages for followers_count
            result_data = []
            for month_data in sorted(monthly_data.values(), key=lambda x: x['month']):
                if month_data['_count'] > 0:
                    month_data['followers_count'] = month_data['followers_count'] // month_data['_count']
                del month_data['_count']
                result_data.append(month_data)
            
            return result_data
            
        except Exception as e:
            print(f"Error getting monthly account stats: {e}")
            return []
    
    async def get_monthly_media_aggregation(self, ig_user_id: str, year: Optional[int] = None) -> List[Dict]:
        """Get monthly aggregated media statistics"""
        try:
            # Get media posts first
            posts_query = self.client.table('media_posts').select('*').eq('ig_user_id', ig_user_id)
            
            if year:
                start_date = f"{year}-01-01T00:00:00Z"
                end_date = f"{year}-12-31T23:59:59Z"
                posts_query = posts_query.gte('timestamp', start_date).lte('timestamp', end_date)
            
            posts_result = posts_query.execute()
            
            # Get all media stats
            stats_result = self.client.table('daily_media_stats').select('*').execute()
            
            # Create lookup for stats
            stats_lookup = {}
            for stat in stats_result.data:
                media_id = stat['ig_media_id']
                if media_id not in stats_lookup:
                    stats_lookup[media_id] = stat
                # Use latest stats if multiple entries
                elif stat['date'] > stats_lookup[media_id]['date']:
                    stats_lookup[media_id] = stat
            
            # Group by month
            monthly_data = {}
            for post in posts_result.data:
                timestamp = post['timestamp']
                month = timestamp[:7]  # "2023-04"
                
                if month not in monthly_data:
                    monthly_data[month] = {
                        'month': month,
                        'media_count': 0,
                        'total_likes': 0,
                        'total_comments': 0,
                        'total_shares': 0,
                        'total_saved': 0
                    }
                
                monthly_data[month]['media_count'] += 1
                
                # Add stats if available
                media_id = post['ig_media_id']
                if media_id in stats_lookup:
                    stats = stats_lookup[media_id]
                    monthly_data[month]['total_likes'] += stats.get('like_count', 0)
                    monthly_data[month]['total_comments'] += stats.get('comments_count', 0)
                    monthly_data[month]['total_shares'] += stats.get('shares', 0)
                    monthly_data[month]['total_saved'] += stats.get('saved', 0)
            
            return sorted(monthly_data.values(), key=lambda x: x['month'])
            
        except Exception as e:
            print(f"Error getting monthly media aggregation: {e}")
            return []
    
    async def get_total_posts_count(self, ig_user_id: str, year: Optional[int] = None) -> int:
        """Get total posts count for the account"""
        try:
            query = self.client.table('media_posts').select('ig_media_id', count='exact').eq('ig_user_id', ig_user_id)
            
            if year:
                start_date = f"{year}-01-01T00:00:00Z"
                end_date = f"{year}-12-31T23:59:59Z"
                query = query.gte('timestamp', start_date).lte('timestamp', end_date)
            
            result = query.execute()
            return result.count if result.count else 0
            
        except Exception as e:
            print(f"Error getting total posts count: {e}")
            return 0
    
    async def get_latest_account_insights(self, ig_user_ids: List[str]) -> Dict[str, Dict]:
        """Get latest account insights for multiple accounts"""
        try:
            latest_insights = {}
            
            for ig_user_id in ig_user_ids:
                result = self.client.table('daily_account_stats').select('*').eq('ig_user_id', ig_user_id).order('date', desc=True).limit(1).execute()
                
                if result.data:
                    latest_insights[ig_user_id] = result.data[0]
                else:
                    # Default empty insights
                    latest_insights[ig_user_id] = {
                        'profile_views': None,
                        'website_clicks': None,
                        'followers_count': None,
                        'follows_count': None,
                        'media_count': None
                    }
            
            return latest_insights
        except Exception as e:
            print(f"Error getting latest account insights: {e}")
            return {}
    
    async def get_daily_account_stats(self, ig_user_id: str, year: int, month: int) -> List[Dict]:
        """Get daily account statistics for a specific month"""
        try:
            from calendar import monthrange
            
            # Calculate date range for the month
            start_date = f"{year}-{month:02d}-01"
            days_in_month = monthrange(year, month)[1]
            end_date = f"{year}-{month:02d}-{days_in_month:02d}"
            
            # Get daily account stats for the month
            query = self.client.table('daily_account_stats').select('*')
            query = query.eq('ig_user_id', ig_user_id)
            query = query.gte('date', start_date).lte('date', end_date)
            result = query.order('date').execute()
            
            # Fill missing days with zero data
            return self._fill_missing_account_days(result.data, year, month)
            
        except Exception as e:
            print(f"Error getting daily account stats: {e}")
            return []
    
    async def get_daily_media_stats_aggregation(self, ig_user_id: str, year: int, month: int) -> List[Dict]:
        """Get daily media statistics aggregation for a specific month"""
        try:
            from calendar import monthrange
            
            # Calculate date range for the month
            start_date = f"{year}-{month:02d}-01T00:00:00Z"
            days_in_month = monthrange(year, month)[1]
            end_date = f"{year}-{month:02d}-{days_in_month:02d}T23:59:59Z"
            
            # Get media posts for the month
            posts_query = self.client.table('media_posts').select('*').eq('ig_user_id', ig_user_id)
            posts_query = posts_query.gte('timestamp', start_date).lte('timestamp', end_date)
            posts_result = posts_query.execute()
            
            # Get all media stats
            stats_result = self.client.table('daily_media_stats').select('*').execute()
            
            # Create lookup for stats
            stats_lookup = {}
            for stat in stats_result.data:
                media_id = stat['ig_media_id']
                if media_id not in stats_lookup:
                    stats_lookup[media_id] = stat
                elif stat['date'] > stats_lookup[media_id]['date']:
                    stats_lookup[media_id] = stat
            
            # Group posts by day and calculate daily totals
            daily_data = {}
            for post in posts_result.data:
                timestamp = post['timestamp']
                date = timestamp[:10]  # "2025-03-01"
                
                if date not in daily_data:
                    daily_data[date] = {
                        'date': date,
                        'posts_count': 0,
                        'reach': 0
                    }
                
                daily_data[date]['posts_count'] += 1
                
                # Add stats if available
                media_id = post['ig_media_id']
                if media_id in stats_lookup:
                    stats = stats_lookup[media_id]
                    daily_data[date]['reach'] += stats.get('reach', 0)
            
            # Fill missing days and sort
            return self._fill_missing_media_days(list(daily_data.values()), year, month)
            
        except Exception as e:
            print(f"Error getting daily media stats aggregation: {e}")
            return []
    
    def _fill_missing_account_days(self, data: List[Dict], year: int, month: int) -> List[Dict]:
        """Fill missing days with zero data for account stats"""
        from calendar import monthrange
        
        days_in_month = monthrange(year, month)[1]
        filled_data = []
        
        # Create lookup for existing data
        data_lookup = {d['date']: d for d in data}
        
        for day in range(1, days_in_month + 1):
            date_str = f"{year}-{month:02d}-{day:02d}"
            
            if date_str in data_lookup:
                # Use existing data
                filled_data.append(data_lookup[date_str])
            else:
                # Zero-fill missing data
                filled_data.append({
                    'date': date_str,
                    'posts_count': 0,
                    'new_followers': 0,
                    'reach': 0,
                    'profile_views': 0,
                    'website_clicks': 0
                })
        
        return filled_data
    
    def _fill_missing_media_days(self, data: List[Dict], year: int, month: int) -> List[Dict]:
        """Fill missing days with zero data for media stats"""
        from calendar import monthrange
        
        days_in_month = monthrange(year, month)[1]
        filled_data = []
        
        # Create lookup for existing data
        data_lookup = {d['date']: d for d in data}
        
        for day in range(1, days_in_month + 1):
            date_str = f"{year}-{month:02d}-{day:02d}"
            
            if date_str in data_lookup:
                # Use existing data
                filled_data.append(data_lookup[date_str])
            else:
                # Zero-fill missing data
                filled_data.append({
                    'date': date_str,
                    'posts_count': 0,
                    'reach': 0
                })
        
        return filled_data

# Repository instance
instagram_repository = InstagramAccountRepository()