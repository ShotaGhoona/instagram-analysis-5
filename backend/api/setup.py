from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from models.database import db_manager
from utils.instagram_client import InstagramAPIClient
from auth.simple_auth import get_current_user, User

router = APIRouter(prefix="/setup", tags=["setup"])

class TokenRefreshRequest(BaseModel):
    app_id: str
    app_secret: str
    access_token: str

class TokenRefreshResponse(BaseModel):
    success: bool
    message: str
    updated_accounts: int
    new_accounts: int
    total_processed: int
    errors: list = []

@router.post("/refresh-tokens", response_model=TokenRefreshResponse)
async def refresh_tokens(
    request: TokenRefreshRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Instagram API認証情報を使ってアカウントトークンをリフレッシュ
    
    - Facebook Graph APIで管理ページを取得
    - Instagram Business Accountを特定
    - Page Access Tokenを長期トークンに変換
    - データベースに新規作成または更新
    """
    print(f"🚀 トークンリフレッシュ開始 - ユーザー: {current_user.username}")
    
    try:
        # Instagram APIクライアント初期化
        client = InstagramAPIClient(
            app_id=request.app_id,
            app_secret=request.app_secret,
            access_token=request.access_token
        )
        
        # 全アカウントのトークンリフレッシュを実行
        refresh_result = client.refresh_all_account_tokens()
        
        if not refresh_result["success"]:
            raise HTTPException(
                status_code=400,
                detail=f"Token refresh failed: {refresh_result.get('error', 'Unknown error')}"
            )
        
        refresh_data = refresh_result["data"]
        updated_accounts = refresh_data["updated_accounts"]
        
        # データベースに保存
        new_accounts_count = 0
        updated_accounts_count = 0
        db_errors = []
        
        for account_data in updated_accounts:
            try:
                result = await db_manager.upsert_instagram_account(account_data)
                if result:
                    # 新規 or 更新判定
                    existing = await db_manager.get_instagram_account(account_data['ig_user_id'])
                    if existing:
                        updated_accounts_count += 1
                        print(f"   ✅ 更新: @{account_data['username']}")
                    else:
                        new_accounts_count += 1
                        print(f"   🆕 新規: @{account_data['username']}")
                else:
                    error_msg = f"Database save failed for account: {account_data['username']}"
                    db_errors.append(error_msg)
                    print(f"   ❌ DB保存失敗: @{account_data['username']}")
            except Exception as e:
                error_msg = f"Database error for {account_data['username']}: {str(e)}"
                db_errors.append(error_msg)
                print(f"   ❌ DB例外: @{account_data['username']} - {str(e)}")
        
        # 最終的な件数調整（既存チェックが非同期で正確でない場合があるため簡略化）
        if new_accounts_count == 0 and updated_accounts_count == 0 and len(updated_accounts) > 0:
            updated_accounts_count = len(updated_accounts)
        
        all_errors = refresh_data.get("errors", []) + db_errors
        
        success_message = f"Token refresh completed: {len(updated_accounts)} accounts processed"
        if len(all_errors) > 0:
            success_message += f", {len(all_errors)} errors occurred"
        
        print(f"🏁 トークンリフレッシュ完了")
        print(f"📊 新規アカウント: {new_accounts_count}")
        print(f"📊 更新アカウント: {updated_accounts_count}")  
        print(f"📊 エラー数: {len(all_errors)}")
        
        return TokenRefreshResponse(
            success=True,
            message=success_message,
            updated_accounts=updated_accounts_count,
            new_accounts=new_accounts_count,
            total_processed=refresh_data["total_processed"],
            errors=all_errors
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ セットアップAPI例外: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )