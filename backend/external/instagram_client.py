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
        """Make API request and return JSON response with enhanced error handling"""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            error_data = None
            status_code = getattr(e.response, 'status_code', None)
            
            # Parse error response
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                except:
                    error_data = {"error": e.response.text}
            
            # Classify Instagram API errors
            error_message = self._classify_instagram_error(status_code, error_data)
            
            # Structure error response
            error_response = {
                "success": False, 
                "error": error_message,
                "status_code": status_code,
                "error_data": error_data,
                "error_type": self._get_error_type(status_code)
            }
            
            # Log structured error
            self._log_api_error(url, params, error_response)
            
            return error_response
    
    def _classify_instagram_error(self, status_code: int, error_data: dict) -> str:
        """Classify Instagram API errors and return Japanese message"""
        if status_code == 401:
            return "アクセストークンが無効または期限切れです。トークンを更新してください。"
        elif status_code == 403:
            return "このリソースにアクセスする権限がありません。アカウント設定を確認してください。"
        elif status_code == 429:
            return "API呼び出し制限に達しました。しばらく待ってから再試行してください。"
        elif status_code == 400:
            error_msg = "リクエストパラメータが不正です。"
            if error_data and 'error' in error_data:
                error_msg += f" 詳細: {error_data['error']}"
            return error_msg
        elif status_code and 500 <= status_code < 600:
            return "Instagram APIサーバーで一時的な問題が発生しています。しばらく待ってから再試行してください。"
        else:
            return f"Instagram API呼び出しに失敗しました（ステータス: {status_code}）"
    
    def _get_error_type(self, status_code: int) -> str:
        """Get error type for structured logging"""
        if status_code == 401:
            return "TOKEN_EXPIRED"
        elif status_code == 403:
            return "PERMISSION_DENIED"
        elif status_code == 429:
            return "RATE_LIMIT"
        elif status_code == 400:
            return "BAD_REQUEST"
        elif status_code and 500 <= status_code < 600:
            return "SERVER_ERROR"
        else:
            return "UNKNOWN_ERROR"
    
    def _log_api_error(self, url: str, params: dict, error_response: dict):
        """Log API error in structured format"""
        print(f"❌ Instagram API Error: {error_response['error_type']}")
        print(f"   🔗 URL: {url}")
        print(f"   📊 Status: {error_response['status_code']}")
        print(f"   💬 Message: {error_response['error']}")
        if error_response.get('error_data'):
            print(f"   📋 Details: {error_response['error_data']}")
    
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
                'fields': 'id,username,name,profile_picture_url,followers_count,follows_count,media_count',
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
    
    def get_user_media(self, ig_user_id: str, access_token: str, limit: int = 25) -> Dict[str, Any]:
        """Get Instagram media posts for an account"""
        try:
            # 検証済みフィールド構成を使用
            fields = 'id,timestamp,media_type,caption,like_count,comments_count,media_url,thumbnail_url,permalink'
            params = {
                'fields': fields,
                'limit': limit,
                'access_token': access_token
            }
            
            result = self.graph_api_request(f'/{ig_user_id}/media', params)
            
            if result["success"]:
                return result["data"]
            else:
                print(f"   ⚠️ Media posts取得失敗: {result.get('error', 'Unknown error')}")
                return {"success": False, "error": result.get("error", "Unknown error")}
                
        except Exception as e:
            print(f"   ⚠️ Media posts取得例外: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_media_insights(self, ig_media_id: str, access_token: str, metrics: List[str] = None) -> Dict[str, Any]:
        """Get insights for specific media post"""
        try:
            if metrics is None:
                metrics = ['reach', 'shares', 'saved']  # 検証済み基本メトリクス
            
            print(f"🔍 Media Insights取得開始: {ig_media_id[:15]}...")
            insights_result = {}
            
            for metric in metrics:
                print(f"   📊 {metric} メトリクス取得中...")
                try:
                    params = {
                        'metric': metric,
                        'access_token': access_token
                    }
                    
                    result = self.graph_api_request(f'/{ig_media_id}/insights', params)
                    
                    if result["success"] and "data" in result and "data" in result["data"] and len(result["data"]["data"]) > 0:
                        metric_data = result["data"]["data"][0]
                        values = metric_data.get("values", [])
                        if values and len(values) > 0:
                            value = values[0].get("value", 0)
                            insights_result[metric] = {
                                "success": True,
                                "value": value,
                                "raw_data": metric_data
                            }
                            print(f"      ✅ {metric}: {value:,}")
                        else:
                            insights_result[metric] = {
                                "success": False,
                                "error": "Empty values array"
                            }
                            print(f"      ❌ {metric}: データが空")
                    else:
                        insights_result[metric] = {
                            "success": False,
                            "error": result.get("error", "No data in response")
                        }
                        print(f"      ❌ {metric}: {result.get('error', 'レスポンスなし')}")
                        
                except Exception as e:
                    insights_result[metric] = {
                        "success": False,
                        "error": str(e)
                    }
                    print(f"      ❌ {metric}: 例外 - {str(e)}")
            
            success_count = sum(1 for result in insights_result.values() if result.get("success"))
            print(f"✅ Media Insights完了: {success_count}/{len(metrics)} メトリクス成功")
            
            return {
                "success": success_count > 0,
                "data": insights_result,
                "total_metrics": len(metrics),
                "successful_metrics": success_count
            }
            
        except Exception as e:
            print(f"❌ Media Insights取得例外: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_media_insights_with_type(self, ig_media_id: str, media_type: str, access_token: str) -> Dict[str, Any]:
        """Get insights for media with type-specific metrics"""
        try:
            # 基本メトリクス
            metrics = ['reach', 'shares', 'saved']
            
            # VIDEO投稿には views メトリクス追加
            if media_type == 'VIDEO':
                metrics.append('views')
            
            print(f"🎬 {media_type}投稿のインサイト取得: {len(metrics)}メトリクス")
            return self.get_media_insights(ig_media_id, access_token, metrics)
            
        except Exception as e:
            print(f"❌ Type-specific insights取得例外: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_account_insights(self, ig_user_id: str, access_token: str, metrics: List[str] = None) -> Dict[str, Any]:
        """Get account-level insights"""
        try:
            if metrics is None:
                metrics = ['profile_views', 'website_clicks']  # 検証済みメトリクス
            
            print(f"🔍 Account Insights取得開始: {ig_user_id}")
            print(f"   📊 対象メトリクス: {', '.join(metrics)}")
            
            params = {
                'metric': ','.join(metrics),
                'period': 'day',
                'metric_type': 'total_value',  # 必須パラメータ
                'access_token': access_token
            }
            
            result = self.graph_api_request(f'/{ig_user_id}/insights', params)
            
            if result.get("success") and "data" in result:
                insights_data = result["data"]
                
                # Instagram Account Insights の構造: {"data": [insights...]}
                if "data" in insights_data:
                    actual_insights = insights_data["data"]
                else:
                    actual_insights = insights_data
                
                # レスポンスデータを解析
                insights_result = {}
                for insight in actual_insights:
                    metric_name = insight.get('name')
                    
                    # Account Insights の場合、データ構造が異なる
                    if 'total_value' in insight:
                        # Account insights format: {"total_value": {"value": 0}}
                        value = insight['total_value'].get('value', 0)
                        insights_result[metric_name] = {
                            "success": True,
                            "value": value,
                            "raw_data": insight
                        }
                        print(f"      ✅ {metric_name}: {value:,}")
                    elif 'values' in insight:
                        # Media insights format: {"values": [{"value": 0}]}
                        values = insight.get('values', [])
                        if values and len(values) > 0:
                            value = values[0].get('value', 0)
                            end_time = values[0].get('end_time', 'N/A')
                            insights_result[metric_name] = {
                                "success": True,
                                "value": value,
                                "end_time": end_time,
                                "raw_data": insight
                            }
                            print(f"      ✅ {metric_name}: {value:,}")
                        else:
                            insights_result[metric_name] = {
                                "success": False,
                                "error": "Empty values array"
                            }
                            print(f"      ❌ {metric_name}: データが空")
                    else:
                        insights_result[metric_name] = {
                            "success": False,
                            "error": "Unknown data format"
                        }
                        print(f"      ❌ {metric_name}: 不明なデータ形式")
                
                success_count = sum(1 for result in insights_result.values() if result.get("success"))
                print(f"✅ Account Insights完了: {success_count}/{len(metrics)} メトリクス成功")
                
                return {
                    "success": success_count > 0,
                    "data": insights_result,
                    "total_metrics": len(metrics),
                    "successful_metrics": success_count
                }
            else:
                print(f"❌ Account Insights失敗: {result.get('error', 'No data in response')}")
                return {"success": False, "error": result.get("error", "No data in response")}
                
        except Exception as e:
            print(f"❌ Account Insights取得例外: {str(e)}")
            print(f"   🔍 詳細: {type(e).__name__} - {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}

# Create instance for easy import
instagram_client = InstagramAPIClient()