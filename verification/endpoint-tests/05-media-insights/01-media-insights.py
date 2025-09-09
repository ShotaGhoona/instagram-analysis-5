#!/usr/bin/env python3
"""
Media Insights Verification Script

Test GET /{ig-media-id}/insights?metric=reach
Test GET /{ig-media-id}/insights?metric=video_views (for video posts)
for media-specific insights data collection.
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.api_client import InstagramAPIClient

def test_media_insights():
    """Test media insights retrieval for reach and video views metrics"""
    
    print("🚀 Media Insights 検証を開始します")
    print(f"📅 実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print()
    
    # Load Page Access Tokens from 01-me results
    input_file = os.path.join(os.path.dirname(__file__), '..', '01-me', '01-output-data.json')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            me_data = json.load(f)
    except FileNotFoundError:
        print("❌ エラー: ../01-me/01-output-data.json が見つかりません")
        print("   🔧 対策: 先に 01-me/01-basic-user-info.py を実行してください")
        return False
    
    # Extract accounts data
    accounts_data = None
    for test in me_data.get('tests', []):
        if test.get('test_name') == 'user_accounts':
            accounts_data = test.get('data', {}).get('data', [])
            break
    
    if not accounts_data:
        print("❌ エラー: アカウントデータが見つかりません")
        return False
    
    print(f"🔍 検証対象: {len(accounts_data)}件のInstagram Business Account")
    print("   📝 注: 最初の2件をサンプルとしてメディアインサイトを取得します")
    print()
    
    # Results structure
    results = {
        "endpoint": "/{ig-media-id}/insights (Media Insights)",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "投稿別インサイトメトリクス取得テスト",
        "account_tests": []
    }
    
    # Use long-lived tokens from 02-refresh_access_token results
    long_lived_token_file = os.path.join(os.path.dirname(__file__), '..', '02-refresh_access_token', '01-output-data.json')
    try:
        with open(long_lived_token_file, 'r', encoding='utf-8') as f:
            token_data = json.load(f)
        
        # Update tokens for all accounts
        for account in accounts_data:
            page_name = account.get('name')
            for conversion in token_data.get('token_conversions', []):
                if conversion.get('page_name') == page_name:
                    long_lived_token = conversion.get('page_long_lived_token', {}).get('token')
                    if long_lived_token:
                        account['access_token'] = long_lived_token
                        print(f"🔑 {page_name}: 長期トークン適用")
                    break
        
        print()
            
    except FileNotFoundError:
        print(f"⚠️ 長期トークンファイルなし、既存トークンを使用")
        print()
    
    client = InstagramAPIClient()
    
    # Process first 2 accounts as sample
    sample_count = min(2, len(accounts_data))
    
    for i in range(sample_count):
        account = accounts_data[i]
        page_name = account.get('name', 'Unknown')
        page_id = account.get('id', 'Unknown')
        ig_account_id = account.get('instagram_business_account', {}).get('id', '')
        page_token = account.get('access_token', '')
        
        print(f"🔍 テスト {i+1}/{sample_count}: {page_name}")
        print(f"   📄 Page ID: {page_id}")
        print(f"   📸 IG Account ID: {ig_account_id}")
        
        if not ig_account_id or not page_token:
            print(f"   ⚠️ 警告: Instagram Account IDまたはTokenが不足")
            continue
        
        account_result = {
            "page_name": page_name,
            "page_id": page_id,
            "ig_account_id": ig_account_id,
            "tests": []
        }
        
        # First, get some media posts to test insights on
        print(f"   🔍 ステップ1: 投稿データを取得中...")
        try:
            media_params = {
                'fields': 'id,media_type,timestamp',
                'limit': 5,  # Get first 5 posts for insights testing
                'access_token': page_token
            }
            
            media_response = client.graph_api_request(f'/{ig_account_id}/media', params=media_params)
            
            if not media_response or 'data' not in media_response:
                print(f"   ❌ 投稿データの取得に失敗")
                continue
            
            media_list = media_response['data']
            print(f"   ✅ {len(media_list)}件の投稿データを取得")
            
            # Test insights for each media
            insights_results = []
            
            for idx, media in enumerate(media_list[:3]):  # Test first 3 media
                media_id = media.get('id')
                media_type = media.get('media_type')
                timestamp = media.get('timestamp')
                
                print(f"   🧪 投稿{idx+1}: {media_type} ({media_id[:15]}...)")
                
                media_insights = {
                    "media_id": media_id,
                    "media_type": media_type,
                    "timestamp": timestamp,
                    "insights": {}
                }
                
                # Test 1: Reach insights (for all media types)
                print(f"      📊 テスト: リーチ取得...")
                try:
                    reach_params = {
                        'metric': 'reach',
                        'access_token': page_token
                    }
                    
                    reach_response = client.graph_api_request(f'/{media_id}/insights', params=reach_params)
                    
                    if reach_response and 'data' in reach_response:
                        reach_data = reach_response['data']
                        if reach_data and len(reach_data) > 0:
                            reach_value = reach_data[0].get('values', [{}])[0].get('value', 0)
                            media_insights["insights"]["reach"] = {
                                "success": True,
                                "value": reach_value,
                                "raw_data": reach_data[0]
                            }
                            print(f"         ✅ リーチ: {reach_value:,} ユーザー")
                        else:
                            media_insights["insights"]["reach"] = {
                                "success": False,
                                "error": "Empty data array"
                            }
                            print(f"         ❌ リーチ: データが空")
                    else:
                        media_insights["insights"]["reach"] = {
                            "success": False,
                            "error": "No response or missing data key"
                        }
                        print(f"         ❌ リーチ: レスポンスなし")
                        
                except Exception as e:
                    media_insights["insights"]["reach"] = {
                        "success": False,
                        "error": str(e)
                    }
                    print(f"         ❌ リーチ: 例外 - {e}")
                
                # Test 2: Video views (only for VIDEO media)
                if media_type == 'VIDEO':
                    print(f"      🎬 テスト: 動画視聴数取得...")
                    try:
                        video_params = {
                            'metric': 'video_views',
                            'access_token': page_token
                        }
                        
                        video_response = client.graph_api_request(f'/{media_id}/insights', params=video_params)
                        
                        if video_response and 'data' in video_response:
                            video_data = video_response['data']
                            if video_data and len(video_data) > 0:
                                video_value = video_data[0].get('values', [{}])[0].get('value', 0)
                                media_insights["insights"]["video_views"] = {
                                    "success": True,
                                    "value": video_value,
                                    "raw_data": video_data[0]
                                }
                                print(f"         ✅ 動画視聴数: {video_value:,} 回")
                            else:
                                media_insights["insights"]["video_views"] = {
                                    "success": False,
                                    "error": "Empty data array"
                                }
                                print(f"         ❌ 動画視聴数: データが空")
                        else:
                            media_insights["insights"]["video_views"] = {
                                "success": False,
                                "error": "No response or missing data key"
                            }
                            print(f"         ❌ 動画視聴数: レスポンスなし")
                            
                    except Exception as e:
                        media_insights["insights"]["video_views"] = {
                            "success": False,
                            "error": str(e)
                        }
                        print(f"         ❌ 動画視聴数: 例外 - {e}")
                else:
                    print(f"      ⏭️  動画視聴数: {media_type}のためスキップ")
                    media_insights["insights"]["video_views"] = {
                        "success": False,
                        "error": f"Not applicable for {media_type}"
                    }
                
                insights_results.append(media_insights)
            
            # Create test result
            test_result = {
                "test_name": "media_insights",
                "success": len(insights_results) > 0,
                "data": {
                    "media_count": len(media_list),
                    "tested_media": insights_results
                },
                "notes": f"{len(insights_results)}件の投稿でインサイト検証完了"
            }
            
        except Exception as e:
            test_result = {
                "test_name": "media_insights",
                "success": False,
                "error": str(e),
                "notes": "メディアインサイト取得で例外発生"
            }
            print(f"   ❌ 例外: {e}")
        
        account_result["tests"].append(test_result)
        results["account_tests"].append(account_result)
        print()
    
    # Save results
    output_file = os.path.join(os.path.dirname(__file__), '01-output-data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 結果保存: {output_file}")
    
    # Summary
    total_accounts = len(results["account_tests"])
    successful_accounts = 0
    total_reach_tests = 0
    successful_reach_tests = 0
    total_video_tests = 0
    successful_video_tests = 0
    
    for account in results["account_tests"]:
        account_success = False
        for test in account.get("tests", []):
            if test.get("test_name") == "media_insights" and test.get("success"):
                account_success = True
                tested_media = test.get("data", {}).get("tested_media", [])
                
                for media in tested_media:
                    # Count reach tests
                    reach_insight = media.get("insights", {}).get("reach")
                    if reach_insight:
                        total_reach_tests += 1
                        if reach_insight.get("success"):
                            successful_reach_tests += 1
                    
                    # Count video tests
                    video_insight = media.get("insights", {}).get("video_views")
                    if video_insight and media.get("media_type") == "VIDEO":
                        total_video_tests += 1
                        if video_insight.get("success"):
                            successful_video_tests += 1
                break
        
        if account_success:
            successful_accounts += 1
    
    print(f"\n🏁 検証完了 - 実行結果サマリー")
    print(f"📊 総アカウント数: {total_accounts}")
    print(f"✅ 成功したアカウント: {successful_accounts}")
    print(f"❌ 失敗したアカウント: {total_accounts - successful_accounts}")
    print(f"📈 リーチ取得: {successful_reach_tests}/{total_reach_tests} 件成功")
    print(f"🎬 動画視聴数取得: {successful_video_tests}/{total_video_tests} 件成功")
    
    if successful_accounts > 0:
        print("🎉 メディアインサイトの取得に成功しました！")
        print("🔍 次のステップ: 投稿分析ページでリーチ・動画視聴数データを活用できます")
        return True
    else:
        print("⚠️ メディアインサイトの取得に失敗しました")
        print("🔧 対策: Page Access Tokenとinsights権限の設定を確認してください")
        return False

if __name__ == "__main__":
    success = test_media_insights()
    sys.exit(0 if success else 1)