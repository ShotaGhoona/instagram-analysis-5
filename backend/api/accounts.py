from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from pydantic import BaseModel
from models.instagram import InstagramAccount
from models.user import User
from repositories.instagram_repository import instagram_repository
from middleware.auth.simple_auth import get_current_user

router = APIRouter()

class InstagramAccountCreate(BaseModel):
    name: str
    ig_user_id: str
    access_token: str
    username: str
    profile_picture_url: Optional[str] = None

class InstagramAccountResponse(BaseModel):
    id: int
    name: str
    ig_user_id: str
    username: str
    profile_picture_url: Optional[str] = None

@router.get("/", response_model=List[InstagramAccountResponse])
async def get_accounts(current_user: User = Depends(get_current_user)):
    """全てのInstagramアカウント一覧を取得"""
    accounts = await instagram_repository.get_all()
    return [
        InstagramAccountResponse(
            id=account.id,
            name=account.name,
            ig_user_id=account.ig_user_id,
            username=account.username,
            profile_picture_url=account.profile_picture_url
        ) for account in accounts
    ]

@router.get("/{ig_user_id}", response_model=InstagramAccountResponse)
async def get_account(ig_user_id: str, current_user: User = Depends(get_current_user)):
    """特定のInstagramアカウント詳細を取得"""
    account = await instagram_repository.get_by_id(ig_user_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram account not found"
        )
    
    return InstagramAccountResponse(
        id=account.id,
        name=account.name,
        ig_user_id=account.ig_user_id,
        username=account.username,
        profile_picture_url=account.profile_picture_url
    )

@router.post("/", response_model=InstagramAccountResponse)
async def create_account(
    account_data: InstagramAccountCreate,
    current_user: User = Depends(get_current_user)
):
    """新しいInstagramアカウントを追加"""
    account = InstagramAccount(
        name=account_data.name,
        ig_user_id=account_data.ig_user_id,
        access_token=account_data.access_token,
        username=account_data.username,
        profile_picture_url=account_data.profile_picture_url
    )
    
    created_account = await instagram_repository.create(account)
    if not created_account:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create Instagram account"
        )
    
    return InstagramAccountResponse(
        id=created_account.id,
        name=created_account.name,
        ig_user_id=created_account.ig_user_id,
        username=created_account.username,
        profile_picture_url=created_account.profile_picture_url
    )