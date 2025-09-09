import requests
import json
from typing import Dict, Any, Optional, List
import os
from datetime import datetime

class InstagramAPIClient:
    """Instagram API client for token management and account operations"""
    
    def __init__(self, app_id: str = None, app_secret: str = None, access_token: str = None):
        self.app_id = app_id or os.getenv('INSTAGRAM_APP_ID')
        self.app_secret = app_secret or os.getenv('INSTAGRAM_APP_SECRET') 
        self.access_token = access_token or os.getenv('INSTAGRAM_ACCESS_TOKEN')
        
        # Base URLs
        self.graph_api_url = "https://graph.facebook.com/v23.0"
        self.oauth_url = "https://graph.facebook.com/v23.0/oauth/access_token"
    
    def make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request and return JSON response"""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            error_data = None
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                except:
                    error_data = {"error": e.response.text}
            
            return {
                "success": False, 
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None),
                "error_data": error_data
            }
    
    def graph_api_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make request to Facebook Graph API"""
        if params is None:
            params = {}
        
        if 'access_token' not in params:
            params['access_token'] = self.access_token
        
        # Remove leading slash from endpoint to avoid double slashes
        endpoint = endpoint.lstrip('/')
        url = f"{self.graph_api_url}/{endpoint}"
        return self.make_request(url, params)
    
    def get_user_pages(self) -> Dict[str, Any]:
        """Get user's Facebook pages with Instagram Business Accounts"""
        return self.graph_api_request('/me/accounts', {
            'fields': 'id,name,access_token,instagram_business_account'
        })
    
    def exchange_token_to_long_lived(self, page_access_token: str) -> Dict[str, Any]:
        """Convert Page Access Token to long-lived token"""
        try:
            params = {
                'grant_type': 'fb_exchange_token',
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'fb_exchange_token': page_access_token
            }
            
            response = requests.get(self.oauth_url, params=params)
            
            if response.status_code == 200:
                token_data = response.json()
                return {
                    "success": True,
                    "data": {
                        "access_token": token_data.get('access_token'),
                        "token_type": token_data.get('token_type', 'bearer'),
                        "expires_in": token_data.get('expires_in', 0),
                        "generated_at": datetime.now().isoformat()
                    }
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                return {
                    "success": False,
                    "error": f"Token exchange failed: {response.status_code}",
                    "error_data": error_data
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Token exchange exception: {str(e)}"
            }
    
    def refresh_all_account_tokens(self) -> Dict[str, Any]:
        """Refresh tokens for all accessible Instagram Business Accounts"""
        print("🚀 Instagram Account Token Refresh開始")
        print(f"📅 実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        
        # Get user pages
        pages_result = self.get_user_pages()
        if not pages_result["success"]:
            return {
                "success": False,
                "error": "Failed to get user pages",
                "error_details": pages_result
            }
        
        pages_data = pages_result["data"].get("data", [])
        print(f"🔍 発見されたページ数: {len(pages_data)}")
        
        # Process each page
        updated_accounts = []
        new_accounts = []
        errors = []
        
        for page in pages_data:
            page_name = page.get('name', 'Unknown')
            page_id = page.get('id', '')
            page_token = page.get('access_token', '')
            ig_account = page.get('instagram_business_account', {})
            ig_account_id = ig_account.get('id', '') if ig_account else ''
            
            print(f"\n🔍 処理中: {page_name}")
            print(f"   📄 Page ID: {page_id}")
            print(f"   📸 IG Account ID: {ig_account_id}")
            
            if not ig_account_id or not page_token:
                error_msg = f"Instagram Business Account not found for page: {page_name}"
                print(f"   ⚠️ スキップ: {error_msg}")
                errors.append({
                    "page_name": page_name,
                    "page_id": page_id,
                    "error": error_msg
                })
                continue
            
            # Exchange to long-lived token
            token_result = self.exchange_token_to_long_lived(page_token)
            if not token_result["success"]:
                error_msg = f"Token exchange failed: {token_result.get('error', 'Unknown error')}"
                print(f"   ❌ 失敗: {error_msg}")
                errors.append({
                    "page_name": page_name,
                    "page_id": page_id,
                    "ig_account_id": ig_account_id,
                    "error": error_msg
                })
                continue
            
            # Get Instagram account info using the long-lived token
            ig_info_result = self.get_instagram_account_info(ig_account_id, token_result["data"]["access_token"])
            
            account_data = {
                "page_name": page_name,
                "page_id": page_id,
                "ig_user_id": ig_account_id,
                "access_token": token_result["data"]["access_token"],
                "username": ig_info_result.get("username", page_name),
                "profile_picture_url": ig_info_result.get("profile_picture_url"),
                "token_expires_in": token_result["data"]["expires_in"],
                "token_generated_at": token_result["data"]["generated_at"]
            }
            
            print(f"   ✅ 成功: トークンを更新しました")
            print(f"      👤 Username: @{account_data['username']}")
            
            # 新規 or 更新判定は呼び出し元で行う
            updated_accounts.append(account_data)
        
        total_accounts = len(updated_accounts)
        total_errors = len(errors)
        
        print(f"\n🏁 Token Refresh完了")
        print(f"📊 総処理数: {len(pages_data)}")
        print(f"✅ 成功: {total_accounts}")
        print(f"❌ 失敗: {total_errors}")
        
        return {
            "success": True,
            "data": {
                "updated_accounts": updated_accounts,
                "total_processed": len(pages_data),
                "success_count": total_accounts,
                "error_count": total_errors,
                "errors": errors
            }
        }
    
    def get_instagram_account_info(self, ig_account_id: str, access_token: str) -> Dict[str, Any]:
        """Get Instagram account basic info"""
        try:
            result = self.graph_api_request(f'/{ig_account_id}', {
                'fields': 'id,username,account_type,media_count,followers_count,follows_count,profile_picture_url',
                'access_token': access_token
            })
            
            if result["success"]:
                return result["data"]
            else:
                print(f"   ⚠️ Instagram account info取得失敗: {result.get('error', 'Unknown error')}")
                return {}
                
        except Exception as e:
            print(f"   ⚠️ Instagram account info取得例外: {str(e)}")
            return {}

# Create instance for easy import
instagram_client = InstagramAPIClient()