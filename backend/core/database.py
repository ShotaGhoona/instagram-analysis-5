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
            if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
                print("❌ Error: Cannot create Supabase client - missing environment variables")
                return None
            # Use SERVICE_KEY for complex queries in production
            key = settings.SUPABASE_SERVICE_KEY if settings.SUPABASE_SERVICE_KEY else settings.SUPABASE_ANON_KEY
            self._client = create_client(
                settings.SUPABASE_URL,
                key
            )
        return self._client

# Global database connection instance
database = DatabaseConnection()