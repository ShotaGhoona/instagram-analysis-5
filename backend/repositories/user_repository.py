from typing import Optional, List
from models.user import User
from repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """User data access repository"""
    
    def __init__(self):
        super().__init__("users")
    
    async def create(self, user: User) -> Optional[User]:
        """Create a new user"""
        try:
            result = self.client.table(self.table_name).insert({
                'username': user.username,
                'password_hash': user.password_hash
            }).execute()
            return User(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            result = self.client.table(self.table_name).select('*').eq('id', user_id).execute()
            return User(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            result = self.client.table(self.table_name).select('*').eq('username', username).execute()
            return User(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None
    
    async def get_all(self) -> List[User]:
        """Get all users"""
        try:
            result = self.client.table(self.table_name).select('*').execute()
            return [User(**user) for user in result.data]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
    
    async def update(self, user_id: str, update_data: dict) -> Optional[User]:
        """Update user by ID"""
        try:
            result = self.client.table(self.table_name).update(update_data).eq('id', user_id).execute()
            return User(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error updating user: {e}")
            return None
    
    async def delete(self, user_id: str) -> bool:
        """Delete user by ID"""
        try:
            result = self.client.table(self.table_name).delete().eq('id', user_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

# Repository instance
user_repository = UserRepository()