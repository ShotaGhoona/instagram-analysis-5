from supabase import create_client, Client
from core.config import settings

class DatabaseConnection:
    """Supabase database connection manager"""
    
    def __init__(self):
        self._client: Client = None
    
    @property
    def client(self) -> Client:
        """Get Supabase client instance"""
        if self._client is None:
            if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
                print("❌ Error: Cannot create Supabase client - missing environment variables")
                return None
            self._client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
        return self._client

# Global database connection instance
database = DatabaseConnection()