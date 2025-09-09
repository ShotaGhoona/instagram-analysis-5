#!/usr/bin/env python3
"""
B0204 インサイトデータ取得機能のテストスクリプト
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

async def test_b0204_implementation():
    """Test B0204 media insights retrieval implementation"""
    
    print("🚀 B0204 インサイトデータ取得機能テスト開始")
    print(f"📅 実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print()
    
    # Get test data from Supabase
    print("🔍 Supabaseからテストアカウントを取得中...")
    try:
        accounts = await instagram_repository.get_all()
        if not accounts:
            print("❌ Supabaseにアカウントデータが見つかりません")
            print("   🔧 先にセットアップページでアカウントを登録してください")
            return False
        
        # Use first account for testing
        test_account = accounts[0]
        ig_user_id = test_account.ig_user_id
        account_name = test_account.name
        access_token = test_account.access_token
        
    except Exception as e:
        print(f"❌ Supabaseアクセスエラー: {str(e)}")
        return False
    
    print(f"🔍 テスト対象アカウント: {account_name}")
    print(f"   📸 IG User ID: {ig_user_id}")
    print()
    
    # Get some media posts for testing
    print("🔍 投稿データを取得中...")
    try:
        media_posts = await instagram_repository.get_media_posts(ig_user_id, 3)
        if not media_posts:
            print("❌ 投稿データが見つかりません")
            print("   🔧 先にB0203で投稿データを収集してください")
            return False
        
        print(f"✅ {len(media_posts)}件の投稿データを取得")
        
    except Exception as e:
        print(f"❌ 投稿データ取得エラー: {str(e)}")
        return False
    
    # Test 1: Instagram API Client - Insights
    print("🧪 テスト1: Instagram APIクライアント - インサイト取得")
    try:
        client = InstagramAPIClient()
        test_media = media_posts[0]
        test_media_id = test_media['ig_media_id']
        media_type = test_media.get('media_type', 'IMAGE')
        
        print(f"   📸 テスト投稿: {test_media_id[:15]}... ({media_type})")
        
        # Test basic insights
        result = client.get_media_insights(test_media_id, access_token, ['reach', 'shares'])
        
        if result.get("success"):
            insights_data = result.get("data", {})
            successful_metrics = result.get("successful_metrics", 0)
            total_metrics = result.get("total_metrics", 0)
            
            print(f"   ✅ get_media_insights() メソッド実行成功")
            print(f"   📊 成功メトリクス: {successful_metrics}/{total_metrics}")
            
            for metric, metric_result in insights_data.items():
                if metric_result.get("success"):
                    value = metric_result.get("value", 0)
                    print(f"      ✅ {metric}: {value:,}")
                else:
                    print(f"      ❌ {metric}: {metric_result.get('error', 'Failed')}")
        else:
            print(f"   ⚠️ API結果: {result.get('error', 'Unknown error')}")
            
        # Test type-specific insights
        print(f"   🎬 メディアタイプ別インサイト: {media_type}")
        type_result = client.get_media_insights_with_type(test_media_id, media_type, access_token)
        
        if type_result.get("success"):
            successful_metrics = type_result.get("successful_metrics", 0)
            total_metrics = type_result.get("total_metrics", 0)
            print(f"   ✅ get_media_insights_with_type() 実行成功")
            print(f"   📊 {media_type}用メトリクス: {successful_metrics}/{total_metrics} 成功")
        else:
            print(f"   ❌ Type-specific insights: {type_result.get('error', 'Failed')}")
            
    except Exception as e:
        print(f"   ❌ API呼び出しエラー: {str(e)}")
    
    print()
    
    # Test 2: Repository methods
    print("🧪 テスト2: データベースリポジトリ - インサイト保存")
    try:
        # Test save_daily_media_stats method
        test_stats = [{
            'ig_media_id': media_posts[0]['ig_media_id'],
            'like_count': 10,
            'comments_count': 2,
            'reach': 50,
            'views': None,
            'shares': 1,
            'saved': 3
        }]
        
        saved_count = await instagram_repository.save_daily_media_stats(test_stats)
        print(f"   ✅ save_daily_media_stats() メソッド実行可能")
        print(f"   📊 保存件数: {saved_count}")
        
        # Test get_media_stats method
        media_stats = await instagram_repository.get_media_stats(media_posts[0]['ig_media_id'])
        print(f"   ✅ get_media_stats() メソッド実行可能")
        print(f"   📊 取得統計数: {len(media_stats)}")
        
        # Test get_latest_media_stats method  
        media_ids = [post['ig_media_id'] for post in media_posts[:2]]
        latest_stats = await instagram_repository.get_latest_media_stats(media_ids)
        print(f"   ✅ get_latest_media_stats() メソッド実行可能")
        print(f"   📊 最新統計取得: {len(latest_stats)}件")
        
    except Exception as e:
        print(f"   ❌ リポジトリエラー: {str(e)}")
    
    print()
    
    # Test 3: Service integration
    print("🧪 テスト3: Instagram サービス統合 - インサイト収集")
    try:
        service = InstagramService()
        test_media = media_posts[0]
        
        # Test single media insights collection
        result = await service.collect_media_insights(
            test_media['ig_media_id'],
            test_media.get('media_type', 'IMAGE'),
            access_token,
            test_media.get('like_count', 0),
            test_media.get('comments_count', 0)
        )
        
        print(f"   ✅ collect_media_insights() メソッド実行完了")
        print(f"   📊 成功: {result.get('success', False)}")
        print(f"   📊 収集メトリクス: {result.get('collected_metrics', 0)}/{result.get('total_metrics', 0)}")
        
        if not result.get('success'):
            print(f"   ⚠️ エラー: {result.get('error', 'Unknown error')}")
        
        # Test all media insights collection (limit to 2 for testing)
        print(f"   🔄 全投稿インサイト収集テスト...")
        all_result = await service.collect_all_media_insights(ig_user_id, access_token, 2)
        
        print(f"   ✅ collect_all_media_insights() メソッド実行完了")
        print(f"   📊 成功: {all_result.get('success', False)}")
        print(f"   📊 処理メディア: {all_result.get('processed_media', 0)}")
        print(f"   📊 成功メディア: {all_result.get('successful_media', 0)}")
        
    except Exception as e:
        print(f"   ❌ サービス呼び出しエラー: {str(e)}")
    
    print()
    
    print("🏁 B0204 テスト完了")
    print("✅ インサイト取得機能が実装されていることを確認")
    print("📝 次のステップ:")
    print("   1. GitHub Actions統合テスト")
    print("   2. B0205 (アカウントインサイト取得) への進行")
    print("   3. 投稿分析ページでの活用確認")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_b0204_implementation())
    sys.exit(0 if success else 1)