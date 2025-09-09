from typing import Optional, List
from models.instagram import InstagramAccount
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

# Repository instance
instagram_repository = InstagramAccountRepository()