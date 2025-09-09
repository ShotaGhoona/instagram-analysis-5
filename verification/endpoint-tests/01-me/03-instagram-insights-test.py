#!/usr/bin/env python3
"""
Instagram Insights test script

Test if we can retrieve Instagram data (media and insights) using Page Access Tokens
This validates if tokens are suitable for the analytics dashboard requirements.
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.api_client import InstagramAPIClient

def test_instagram_insights():
    """Test Instagram media and insights data retrieval"""
    
    print("🚀 Instagram インサイトデータ取得テストを開始します")
    print(f"📅 テスト実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print()
    
    # Load previous results to get Page Access Tokens
    input_file = os.path.join(os.path.dirname(__file__), '01-output-data.json')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            previous_data = json.load(f)
    except FileNotFoundError:
        print("❌ エラー: 01-output-data.json が見つかりません")
        return False
    
    # Get first Instagram Business Account for testing
    accounts_data = None
    for test in previous_data.get('tests', []):
        if test.get('test_name') == 'user_accounts':
            accounts_data = test.get('data', {}).get('data', [])
            break
    
    if not accounts_data:
        print("❌ エラー: アカウントデータが見つかりません")
        return False
    
    # Use first account for testing
    test_account = accounts_data[0]
    page_name = test_account.get('name', 'Unknown')
    page_id = test_account.get('id', 'Unknown')
    ig_account_id = test_account.get('instagram_business_account', {}).get('id', '')
    page_token = test_account.get('access_token', '')
    
    print(f"🎯 テスト対象アカウント: {page_name}")
    print(f"   📄 Facebook Page ID: {page_id}")
    print(f"   📸 Instagram Business Account ID: {ig_account_id}")
    print()
    
    # Results structure
    results = {
        "endpoint": "Instagram Media & Insights",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "投稿分析ページ用データ取得テスト",
        "test_account": {
            "page_name": page_name,
            "page_id": page_id,
            "ig_account_id": ig_account_id
        },
        "tests": []
    }
    
    # Test 1: Get Instagram Business Account info
    print("🔍 テスト1: Instagram Business Account 基本情報取得")
    try:
        ig_user_url = f"https://graph.facebook.com/v23.0/{ig_account_id}"
        ig_user_params = {
            'fields': 'id,username,media_count,followers_count',
            'access_token': page_token
        }
        
        response = requests.get(ig_user_url, params=ig_user_params)
        response.raise_for_status()
        ig_user_data = response.json()
        
        test_result = {
            "test_name": "ig_user_info",
            "success": True,
            "data": ig_user_data,
            "notes": "Instagram Business Account基本情報取得成功"
        }
        
        username = ig_user_data.get('username', 'N/A')
        followers = ig_user_data.get('followers_count', 'N/A')
        media_count = ig_user_data.get('media_count', 'N/A')
        
        print(f"✅ 成功: アカウント情報を取得しました")
        print(f"   📱 ユーザー名: @{username}")
        print(f"   👥 フォロワー数: {followers}")
        print(f"   📊 投稿数: {media_count}")
        
    except Exception as e:
        test_result = {
            "test_name": "ig_user_info",
            "success": False,
            "error": str(e),
            "notes": "Instagram Business Account基本情報取得失敗"
        }
        print(f"❌ エラー: Instagram Business Account情報の取得に失敗")
        print(f"   🔍 詳細: {e}")
    
    results["tests"].append(test_result)
    print()
    
    # Test 2: Get recent media list (for 投稿分析ページ)
    print("🔍 テスト2: 最新メディア一覧取得（投稿分析ページ用）")
    try:
        media_url = f"https://graph.facebook.com/v23.0/{ig_account_id}/media"
        media_params = {
            'fields': 'id,media_type,media_url,thumbnail_url,caption,timestamp,like_count,comments_count,permalink',
            'limit': 5,  # 最新5件のみテスト
            'access_token': page_token
        }
        
        response = requests.get(media_url, params=media_params)
        response.raise_for_status()
        media_data = response.json()
        
        media_list = media_data.get('data', [])
        
        test_result = {
            "test_name": "media_list",
            "success": True,
            "data": media_data,
            "notes": f"最新メディア{len(media_list)}件を取得成功"
        }
        
        print(f"✅ 成功: {len(media_list)}件のメディアを取得しました")
        
        for i, media in enumerate(media_list[:3]):  # 最初の3件のみ表示
            media_type = media.get('media_type', 'UNKNOWN')
            timestamp = media.get('timestamp', '')
            likes = media.get('like_count', 0)
            comments = media.get('comments_count', 0)
            
            # タイムスタンプを日本語形式に変換
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    date_str = dt.strftime('%m/%d')
                except:
                    date_str = 'N/A'
            else:
                date_str = 'N/A'
            
            print(f"   📊 投稿{i+1}: {date_str} | タイプ:{media_type} | いいね:{likes} | コメント:{comments}")
        
    except Exception as e:
        test_result = {
            "test_name": "media_list",
            "success": False,
            "error": str(e),
            "notes": "メディア一覧取得失敗"
        }
        print(f"❌ エラー: メディア一覧の取得に失敗")
        print(f"   🔍 詳細: {e}")
    
    results["tests"].append(test_result)
    print()
    
    # Test 3: Get insights for one media (if media exists)
    if test_result.get("success") and media_list:
        print("🔍 テスト3: メディアインサイト取得（投稿分析ページ用）")
        
        test_media_id = media_list[0]['id']
        media_type = media_list[0].get('media_type', 'UNKNOWN')
        
        try:
            # Check media age - insights may not be available for very recent posts
            media_timestamp = media_list[0].get('timestamp', '')
            print(f"   📅 投稿日時: {media_timestamp}")
            
            # Try basic insights first (supported in v22.0+)
            metrics = 'reach'  # Start with single most reliable metric
            
            insights_url = f"https://graph.facebook.com/v23.0/{test_media_id}/insights"
            insights_params = {
                'metric': metrics,
                'access_token': page_token
            }
            
            print(f"   🔍 リクエストURL: {insights_url}?metric={metrics}")
            
            response = requests.get(insights_url, params=insights_params)
            
            if response.status_code == 200:
                insights_data = response.json()
                insights_list = insights_data.get('data', [])
                
                test_result = {
                    "test_name": "media_insights",
                    "success": True,
                    "data": insights_data,
                    "test_media_id": test_media_id,
                    "notes": f"メディアインサイト{len(insights_list)}件を取得成功"
                }
            else:
                # Handle specific error cases
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                
                test_result = {
                    "test_name": "media_insights",
                    "success": False,
                    "error": error_data,
                    "status_code": response.status_code,
                    "test_media_id": test_media_id,
                    "notes": f"メディアインサイト取得失敗 (ステータス: {response.status_code})"
                }
                
                print(f"❌ エラー: メディアインサイトの取得に失敗")
                print(f"   🔍 ステータス: {response.status_code}")
                
                error_message = error_data.get('error', {}).get('message', 'Unknown error')
                error_code = error_data.get('error', {}).get('code', 'Unknown')
                print(f"   🔍 エラー: {error_message} (コード: {error_code})")
                
                # Provide specific guidance based on error
                if response.status_code == 400:
                    print(f"   💡 ヒント: 投稿が新しすぎる場合、インサイトデータはまだ利用できません（24-48時間後に再試行）")
            
            # Only show success message if actually successful
            if test_result.get("success"):
                print(f"✅ 成功: メディアインサイトを取得しました")
                print(f"   🎯 対象メディア: {test_media_id} ({media_type})")
                
                # Display key metrics for dashboard
                for insight in insights_list:
                    metric_name = insight.get('name', '')
                    values = insight.get('values', [])
                    if values:
                        value = values[0].get('value', 0)
                    if metric_name == 'reach':
                        print(f"   📈 リーチ: {value}")
                    elif metric_name == 'engagement':
                        print(f"   💬 エンゲージメント: {value}")
                    elif metric_name == 'total_interactions':
                        print(f"   🤝 総インタラクション: {value}")
                    elif metric_name == 'plays':
                        print(f"   ▶️ 再生数: {value}")
                    else:
                        print(f"   📊 {metric_name}: {value}")
            
        except Exception as e:
            test_result = {
                "test_name": "media_insights",
                "success": False,
                "error": str(e),
                "test_media_id": test_media_id,
                "notes": "メディアインサイト取得失敗"
            }
            print(f"❌ エラー: メディアインサイトの取得に失敗")
            print(f"   🔍 詳細: {e}")
        
        results["tests"].append(test_result)
        print()
    
    # Save results
    output_file = os.path.join(os.path.dirname(__file__), '03-output-data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 結果保存: {output_file}")
    
    # Summary
    total_tests = len(results["tests"])
    successful_tests = sum(1 for test in results["tests"] if test.get("success"))
    
    print(f"\n🏁 テスト完了 - 実行結果サマリー")
    print(f"📊 総テスト数: {total_tests}")
    print(f"✅ 成功: {successful_tests}")
    print(f"❌ 失敗: {total_tests - successful_tests}")
    
    if successful_tests >= 2:  # アカウント情報 + メディア一覧が取得できれば成功
        print("🎉 投稿分析ページに必要なデータの取得に成功しました！")
        print("🔍 次のステップ: 他のエンドポイント検証またはアプリ開発開始が可能です")
        return True
    else:
        print("⚠️ 投稿分析ページ用データの取得に課題があります")
        return False

if __name__ == "__main__":
    success = test_instagram_insights()
    sys.exit(0 if success else 1)