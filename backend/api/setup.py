from fastapi import APIRouter, HTTPException, Depends

from models.instagram import TokenRefreshRequest, TokenRefreshResponse
from services.instagram_service import InstagramService
from repositories.instagram_repository import instagram_repository
from auth.simple_auth import get_current_user, User

router = APIRouter(prefix="/setup", tags=["setup"])

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
        # Initialize Instagram service with repository
        service = InstagramService(repository=instagram_repository)
        
        # Execute token refresh through service
        result = await service.refresh_all_tokens(request.dict())
        
        if not result.success:
            raise HTTPException(
                status_code=400,
                detail=result.message
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ セットアップAPI例外: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )