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

# Service instance
instagram_service = InstagramService()