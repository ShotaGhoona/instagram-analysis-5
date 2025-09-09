from typing import Dict, Any
from models.instagram import TokenRefreshResponse
from repositories.instagram_repository import InstagramAccountRepository
from external.instagram_client import InstagramAPIClient

class InstagramService:
    """Instagram business logic service"""
    
    def __init__(self, repository: InstagramAccountRepository = None, client: InstagramAPIClient = None):
        self.repository = repository
        self.client = client
    
    async def refresh_all_tokens(self, credentials: Dict[str, str]) -> TokenRefreshResponse:
        """Refresh tokens for all accessible Instagram Business Accounts"""
        print(f"🚀 Instagram Token Refresh Service開始")
        
        # Initialize Instagram API client with provided credentials
        client = InstagramAPIClient(
            app_id=credentials['app_id'],
            app_secret=credentials['app_secret'],
            access_token=credentials['access_token']
        )
        
        # Refresh all account tokens using the client
        refresh_result = client.refresh_all_account_tokens()
        
        if not refresh_result["success"]:
            return TokenRefreshResponse(
                success=False,
                message=f"Token refresh failed: {refresh_result.get('error', 'Unknown error')}",
                updated_accounts=0,
                new_accounts=0,
                total_processed=0,
                errors=[refresh_result.get('error', 'Unknown error')]
            )
        
        refresh_data = refresh_result["data"]
        updated_accounts = refresh_data["updated_accounts"]
        
        # Save to database using repository
        new_accounts_count = 0
        updated_accounts_count = 0
        db_errors = []
        
        for account_data in updated_accounts:
            try:
                result = await self.repository.upsert_account(account_data)
                if result:
                    # Simple counting logic - all successful upserts are considered updates
                    # (exact new vs update distinction requires more complex logic)
                    updated_accounts_count += 1
                    print(f"   ✅ 保存成功: @{account_data['username']}")
                else:
                    error_msg = f"Database save failed for account: {account_data['username']}"
                    db_errors.append(error_msg)
                    print(f"   ❌ DB保存失敗: @{account_data['username']}")
            except Exception as e:
                error_msg = f"Database error for {account_data['username']}: {str(e)}"
                db_errors.append(error_msg)
                print(f"   ❌ DB例外: @{account_data['username']} - {str(e)}")
        
        # Combine errors
        all_errors = refresh_data.get("errors", []) + db_errors
        
        success_message = f"Token refresh completed: {len(updated_accounts)} accounts processed"
        if len(all_errors) > 0:
            success_message += f", {len(all_errors)} errors occurred"
        
        print(f"🏁 Instagram Token Refresh Service完了")
        print(f"📊 処理アカウント: {updated_accounts_count}")
        print(f"📊 エラー数: {len(all_errors)}")
        
        return TokenRefreshResponse(
            success=True,
            message=success_message,
            updated_accounts=updated_accounts_count,
            new_accounts=new_accounts_count,  # Simplified for PoC
            total_processed=refresh_data["total_processed"],
            errors=[str(error) for error in all_errors]
        )
    
    async def collect_media_posts(self, ig_user_id: str, access_token: str, limit: int = 25) -> Dict[str, Any]:
        """Collect media posts from Instagram API and save to database"""
        try:
            print(f"🚀 Media Posts Collection開始: {ig_user_id}")
            
            # Get media posts from Instagram API
            client = InstagramAPIClient()
            api_result = client.get_user_media(ig_user_id, access_token, limit)
            
            if not api_result.get("success", True) or "data" not in api_result:
                return {
                    "success": False,
                    "error": api_result.get("error", "Failed to get media posts"),
                    "collected_posts": 0
                }
            
            media_list = api_result["data"]
            
            # Add ig_user_id to each post for database storage
            for media in media_list:
                media['ig_user_id'] = ig_user_id
            
            # Save to database
            if self.repository:
                saved_count = await self.repository.save_media_posts(media_list)
            else:
                # Fallback to direct repository access
                from repositories.instagram_repository import instagram_repository
                saved_count = await instagram_repository.save_media_posts(media_list)
            
            print(f"✅ Media Posts Collection完了: {len(media_list)}件取得, {saved_count}件保存")
            
            return {
                "success": True,
                "collected_posts": len(media_list),
                "saved_posts": saved_count,
                "data": media_list
            }
            
        except Exception as e:
            print(f"❌ Media Posts Collection失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "collected_posts": 0
            }
    
    async def collect_media_insights(self, ig_media_id: str, media_type: str, access_token: str, like_count: int = 0, comments_count: int = 0) -> Dict[str, Any]:
        """Collect media insights from Instagram API and save to database"""
        try:
            print(f"🚀 Media Insights Collection開始: {ig_media_id[:15]}...")
            
            # Get insights from Instagram API
            client = InstagramAPIClient()
            api_result = client.get_media_insights_with_type(ig_media_id, media_type, access_token)
            
            if not api_result.get("success"):
                return {
                    "success": False,
                    "error": api_result.get("error", "Failed to get media insights"),
                    "collected_metrics": 0
                }
            
            insights_data = api_result.get("data", {})
            
            # Prepare stats data for database
            stats_data = {
                'ig_media_id': ig_media_id,
                'like_count': like_count,
                'comments_count': comments_count
            }
            
            # Add insights metrics
            for metric, result in insights_data.items():
                if result.get("success"):
                    stats_data[metric] = result.get("value")
                else:
                    stats_data[metric] = None
            
            # Save to database
            if self.repository:
                saved_count = await self.repository.save_daily_media_stats([stats_data])
            else:
                # Fallback to direct repository access
                from repositories.instagram_repository import instagram_repository
                saved_count = await instagram_repository.save_daily_media_stats([stats_data])
            
            successful_metrics = api_result.get("successful_metrics", 0)
            total_metrics = api_result.get("total_metrics", 0)
            
            print(f"✅ Media Insights Collection完了: {successful_metrics}/{total_metrics} メトリクス成功, {saved_count}件保存")
            
            return {
                "success": True,
                "collected_metrics": successful_metrics,
                "total_metrics": total_metrics,
                "saved_records": saved_count,
                "insights_data": insights_data
            }
            
        except Exception as e:
            print(f"❌ Media Insights Collection失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "collected_metrics": 0
            }
    
    async def collect_all_media_insights(self, ig_user_id: str, access_token: str, limit: int = 25) -> Dict[str, Any]:
        """Collect insights for all media posts of an account"""
        try:
            print(f"🚀 All Media Insights Collection開始: {ig_user_id}")
            
            # Get media posts first
            media_result = await self.collect_media_posts(ig_user_id, access_token, limit)
            
            if not media_result.get("success"):
                return {
                    "success": False,
                    "error": "Failed to get media posts: " + media_result.get("error", "Unknown error"),
                    "processed_media": 0
                }
            
            media_list = media_result.get("data", [])
            
            # Collect insights for each media
            insights_results = []
            successful_media = 0
            
            for media in media_list:
                media_id = media.get("id")
                media_type = media.get("media_type", "IMAGE")
                like_count = media.get("like_count", 0)
                comments_count = media.get("comments_count", 0)
                
                insights_result = await self.collect_media_insights(
                    media_id, media_type, access_token, like_count, comments_count
                )
                
                if insights_result.get("success"):
                    successful_media += 1
                
                insights_results.append({
                    "media_id": media_id,
                    "media_type": media_type,
                    "result": insights_result
                })
            
            print(f"✅ All Media Insights Collection完了: {successful_media}/{len(media_list)} メディア成功")
            
            return {
                "success": True,
                "processed_media": len(media_list),
                "successful_media": successful_media,
                "insights_results": insights_results
            }
            
        except Exception as e:
            print(f"❌ All Media Insights Collection失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "processed_media": 0
            }

# Service instance
instagram_service = InstagramService()