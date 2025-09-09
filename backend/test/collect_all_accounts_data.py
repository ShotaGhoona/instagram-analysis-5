#!/usr/bin/env python3
"""
全アカウントの投稿データ収集スクリプト
"""

import asyncio
import sys
import os
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(__file__))

from services.instagram_service import instagram_service
from repositories.instagram_repository import instagram_repository

async def collect_all_accounts_data():
    """Collect media posts data for all accounts"""
    
    print("🚀 全アカウント投稿データ収集開始")
    print(f"📅 実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print()
    
    # Get all accounts
    try:
        accounts = await instagram_repository.get_all()
        if not accounts:
            print("❌ アカウントが見つかりません")
            return False
        
        print(f"🔍 対象アカウント: {len(accounts)}件")
        for i, account in enumerate(accounts):
            print(f"   {i+1}. {account.name} (@{account.username})")
        print()
        
    except Exception as e:
        print(f"❌ アカウント取得エラー: {str(e)}")
        return False
    
    # Collect data for each account
    collection_results = []
    
    for i, account in enumerate(accounts):
        print(f"🚀 {i+1}/{len(accounts)}: {account.name} (@{account.username})")
        print(f"   📸 IG User ID: {account.ig_user_id}")
        
        try:
            # Check if already has data
            existing_posts = await instagram_repository.get_media_posts(account.ig_user_id, 50)
            print(f"   📊 既存投稿データ: {len(existing_posts)}件")
            
            if len(existing_posts) > 0:
                print(f"   ⏭️  既にデータ存在 - スキップ")
                collection_results.append({
                    "account": account.name,
                    "status": "existing",
                    "posts": len(existing_posts),
                    "collected": 0
                })
            else:
                print(f"   🔄 投稿データ収集実行中...")
                
                result = await instagram_service.collect_media_posts(
                    account.ig_user_id, 
                    account.access_token, 
                    25  # Get up to 25 posts
                )
                
                if result.get('success'):
                    collected = result.get('collected_posts', 0)
                    saved = result.get('saved_posts', 0)
                    print(f"   ✅ 成功: {collected}件収集, {saved}件保存")
                    
                    collection_results.append({
                        "account": account.name,
                        "status": "success",
                        "posts": saved,
                        "collected": collected
                    })
                else:
                    error = result.get('error', 'Unknown error')
                    print(f"   ❌ 失敗: {error}")
                    
                    collection_results.append({
                        "account": account.name,
                        "status": "failed",
                        "posts": 0,
                        "collected": 0,
                        "error": error
                    })
            
        except Exception as e:
            print(f"   ❌ 例外: {str(e)}")
            collection_results.append({
                "account": account.name,
                "status": "error",
                "posts": 0,
                "collected": 0,
                "error": str(e)
            })
        
        print()
    
    # Summary
    print("🏁 全アカウント投稿データ収集完了")
    print("="*50)
    
    total_accounts = len(collection_results)
    successful_collections = sum(1 for r in collection_results if r["status"] == "success")
    existing_data = sum(1 for r in collection_results if r["status"] == "existing")
    failed_collections = sum(1 for r in collection_results if r["status"] in ["failed", "error"])
    
    print(f"📊 総アカウント数: {total_accounts}")
    print(f"✅ 新規収集成功: {successful_collections}")
    print(f"📁 既存データ: {existing_data}")
    print(f"❌ 失敗: {failed_collections}")
    print()
    
    print("📋 アカウント別結果:")
    for result in collection_results:
        status_emoji = {
            "success": "✅",
            "existing": "📁", 
            "failed": "❌",
            "error": "💥"
        }
        
        emoji = status_emoji.get(result["status"], "❓")
        posts = result["posts"]
        account = result["account"]
        
        if result["status"] == "success":
            collected = result["collected"]
            print(f"   {emoji} {account}: {collected}件収集 → {posts}件保存")
        elif result["status"] == "existing":
            print(f"   {emoji} {account}: {posts}件既存")
        else:
            error = result.get("error", "Unknown")
            print(f"   {emoji} {account}: 失敗 - {error}")
    
    print()
    
    # Check if we have data for insights testing now
    accounts_with_data = [r for r in collection_results if r["posts"] > 0]
    
    if len(accounts_with_data) > 0:
        print(f"🎉 {len(accounts_with_data)}件のアカウントで投稿データ利用可能")
        print("🔄 インサイトテストを実行可能です")
        print()
        print("次のコマンドでインサイトテストを実行:")
        print("   python backend/test_b0204_multi_account.py")
        return True
    else:
        print("⚠️ 投稿データが取得できたアカウントがありません")
        print("🔧 トークンの更新やアカウント設定を確認してください")
        return False

if __name__ == "__main__":
    success = asyncio.run(collect_all_accounts_data())
    sys.exit(0 if success else 1)