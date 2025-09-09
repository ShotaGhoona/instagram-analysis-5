import requests
import json
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class InstagramAPIClient:
    """Instagram API client for verification scripts"""
    
    def __init__(self):
        self.app_id = os.getenv('INSTAGRAM_APP_ID')
        self.app_secret = os.getenv('INSTAGRAM_APP_SECRET')
        self.access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.business_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        
        # Base URLs
        self.basic_display_url = "https://graph.instagram.com"
        self.graph_api_url = "https://graph.facebook.com/v18.0"
    
    def make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request and return JSON response"""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def basic_display_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make request to Instagram Basic Display API"""
        if params is None:
            params = {}
        params['access_token'] = self.access_token
        
        url = f"{self.basic_display_url}/{endpoint}"
        return self.make_request(url, params)
    
    def graph_api_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make request to Instagram Graph API"""
        if params is None:
            params = {}
        params['access_token'] = self.access_token
        
        url = f"{self.graph_api_url}/{endpoint}"
        return self.make_request(url, params)