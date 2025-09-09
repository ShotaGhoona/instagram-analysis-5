#!/usr/bin/env python3
"""
B0204 マルチアカウントテスト - より成熟したアカウントでのテスト
"""

import asyncio
import sys
import os
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(__file__))

from external.instagram_client import InstagramAPIClient
from services.instagram_service import InstagramService
from repositories.instagram_repository import instagram_repository

async def test_b0204_multi_account():
    """Test B0204 with multiple accounts to find one with insights data"""
    
    print("🚀 B0204 マルチアカウント インサイトテスト開始")
    print(f"📅 実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print()
    
    # Get all accounts from Supabase
    print("🔍 Supabaseから全アカウントを取得中...")
    try:
        accounts = await instagram_repository.get_all()
        if not accounts:
            print("❌ Supabaseにアカウントデータが見つかりません")
            return False
        
        print(f"✅ {len(accounts)}件のアカウントを発見")
        for i, account in enumerate(accounts):
            print(f"   {i+1}. {account.name} (@{account.username})")
        
    except Exception as e:
        print(f"❌ Supabaseアクセスエラー: {str(e)}")
        return False
    
    print()
    
    # Test each account to find one with insights data
    successful_tests = []
    
    for i, account in enumerate(accounts):
        print(f"🧪 テスト {i+1}/{len(accounts)}: {account.name} (@{account.username})")
        print(f"   📸 IG User ID: {account.ig_user_id}")
        
        try:
            # Get media posts for this account
            media_posts = await instagram_repository.get_media_posts(account.ig_user_id, 3)
            if not media_posts:
                print(f"   ⚠️ 投稿データなし - スキップ")
                continue
            
            print(f"   📊 投稿数: {len(media_posts)}件")
            
            # Test insights for first post
            test_media = media_posts[0]
            test_media_id = test_media['ig_media_id']
            media_type = test_media.get('media_type', 'IMAGE')
            
            print(f"   🔍 テスト投稿: {test_media_id[:15]}... ({media_type})")
            
            client = InstagramAPIClient()
            
            # Test basic insights (reach only for speed)
            result = client.get_media_insights(test_media_id, account.access_token, ['reach'])
            
            if result.get("success") and result.get("successful_metrics", 0) > 0:
                insights_data = result.get("data", {})
                reach_data = insights_data.get("reach", {})
                
                if reach_data.get("success"):
                    reach_value = reach_data.get("value", 0)
                    print(f"   ✅ インサイト取得成功!")
                    print(f"      📈 リーチ: {reach_value:,} ユーザー")
                    
                    successful_tests.append({
                        "account": account,
                        "media_id": test_media_id,
                        "media_type": media_type,
                        "reach": reach_value
                    })
                    
                    # Test more metrics for successful account
                    print(f"   🔄 追加メトリクステスト...")
                    full_result = client.get_media_insights_with_type(test_media_id, media_type, account.access_token)
                    
                    if full_result.get("success"):
                        full_insights = full_result.get("data", {})
                        metrics_summary = []
                        
                        for metric, metric_result in full_insights.items():
                            if metric_result.get("success"):
                                value = metric_result.get("value", 0)
                                metrics_summary.append(f"{metric}:{value}")
                            else:
                                metrics_summary.append(f"{metric}:失敗")
                        
                        print(f"      📊 全メトリクス: {', '.join(metrics_summary)}")
                        successful_tests[-1]["full_metrics"] = full_insights
                else:
                    print(f"   ❌ リーチデータ取得失敗: {reach_data.get('error', 'Unknown')}")
            else:
                error = result.get("error", "No successful metrics")
                print(f"   ❌ インサイト取得失敗: {error}")
                
        except Exception as e:
            print(f"   ❌ テスト例外: {str(e)}")
        
        print()
    
    # Summary
    print("🏁 マルチアカウントテスト完了")
    print(f"📊 総テスト数: {len(accounts)}")
    print(f"✅ 成功アカウント数: {len(successful_tests)}")
    print()
    
    if successful_tests:
        print("🎉 インサイトデータ取得成功アカウント:")
        for i, test in enumerate(successful_tests):
            account = test["account"]
            print(f"   {i+1}. {account.name} (@{account.username})")
            print(f"      📈 リーチ: {test['reach']:,} ユーザー")
            
            if "full_metrics" in test:
                full_metrics = test["full_metrics"]
                success_count = sum(1 for m in full_metrics.values() if m.get("success"))
                total_count = len(full_metrics)
                print(f"      📊 メトリクス成功率: {success_count}/{total_count}")
        
        print()
        print("🎯 推奨アカウント:")
        best_account = max(successful_tests, key=lambda x: x["reach"])
        account = best_account["account"]
        print(f"   📛 {account.name} (@{account.username})")
        print(f"   📈 最大リーチ: {best_account['reach']:,} ユーザー")
        print(f"   🔧 このアカウントでの詳細テストを推奨")
        
        # Run detailed test on best account
        print()
        print(f"🚀 詳細テスト実行: {account.name}")
        await run_detailed_insights_test(account)
        
        return True
    else:
        print("⚠️ 全アカウントでインサイトデータ取得に失敗")
        print("🔧 考えられる原因:")
        print("   - アクセストークンの期限切れ")
        print("   - インサイト権限の不足")
        print("   - アカウントの投稿履歴不足")
        print("   - Instagram API の制限")
        return False

async def run_detailed_insights_test(account):
    """Run detailed insights test on successful account"""
    try:
        print(f"   🔍 詳細インサイト収集テスト...")
        
        service = InstagramService()
        result = await service.collect_all_media_insights(
            account.ig_user_id, 
            account.access_token, 
            3  # Test on 3 posts
        )
        
        if result.get("success"):
            processed = result.get("processed_media", 0)
            successful = result.get("successful_media", 0)
            print(f"   ✅ サービス層テスト成功")
            print(f"      📊 処理メディア: {processed}")
            print(f"      ✅ 成功メディア: {successful}")
            print(f"      📈 成功率: {successful/processed*100 if processed > 0 else 0:.1f}%")
        else:
            print(f"   ❌ サービス層テスト失敗: {result.get('error', 'Unknown')}")
            
    except Exception as e:
        print(f"   ❌ 詳細テスト例外: {str(e)}")

if __name__ == "__main__":
    success = asyncio.run(test_b0204_multi_account())
    sys.exit(0 if success else 1)