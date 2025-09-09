import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    _instance: Optional['SupabaseClient'] = None
    _client: Optional[Client] = None
    
    def __new__(cls) -> 'SupabaseClient':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            
            if not url or not key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
            
            self._client = create_client(url, key)
    
    @property
    def client(self) -> Client:
        if self._client is None:
            raise RuntimeError("Supabase client not initialized")
        return self._client
    
    async def test_connection(self) -> bool:
        try:
            response = self._client.table('users').select("count", count="exact").execute()
            return True
        except Exception as e:
            print(f"Supabase connection test failed: {e}")
            return False

supabase_client = SupabaseClient()