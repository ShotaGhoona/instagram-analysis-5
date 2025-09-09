#!/usr/bin/env python3
"""
Views Metric Verification Script

Test the new unified 'views' metric that replaced video_views in April 2025
for VIDEO posts (Reels) from ヤマサリノベ account.
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.api_client import InstagramAPIClient

def test_views_metric():
    """Test the new unified views metric on VIDEO posts"""
    
    print("🚀 Views Metric (新統一指標) 検証を開始します")
    print(f"📅 実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print("🔄 2025年4月廃止されたvideo_viewsの代替としてviewsメトリクスをテスト")
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
    
    # Find ヤマサリノベ account specifically
    yamasa_account = None
    for account in accounts_data:
        if account.get('name') == 'ヤマサリノベ':
            yamasa_account = account
            break
    
    if not yamasa_account:
        print("❌ エラー: ヤマサリノベアカウントが見つかりません")
        return False
    
    # Use long-lived token from 02-refresh_access_token results
    long_lived_token_file = os.path.join(os.path.dirname(__file__), '..', '02-refresh_access_token', '01-output-data.json')
    try:
        with open(long_lived_token_file, 'r', encoding='utf-8') as f:
            token_data = json.load(f)
        
        # Find ヤマサリノベ token
        yamasa_token = None
        for conversion in token_data.get('token_conversions', []):
            if conversion.get('page_name') == 'ヤマサリノベ':
                yamasa_token = conversion.get('page_long_lived_token', {}).get('token')
                break
        
        if yamasa_token:
            print(f"🔑 長期トークンを使用: {yamasa_token[:20]}...")
            yamasa_account['access_token'] = yamasa_token
        else:
            print(f"⚠️ 長期トークンが見つからず、既存トークンを使用")
            
    except FileNotFoundError:
        print(f"⚠️ 長期トークンファイルなし、既存トークンを使用")
    
    print(f"🎯 検証対象: ヤマサリノベ - 新しいviews メトリクス検証")
    print("   📝 注: 前回発見した17件のVIDEO投稿でviews メトリクスを検証します")
    print()
    
    # Results structure
    results = {
        "endpoint": "/{ig-media-id}/insights?metric=views (New Unified Metric)",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "2025年4月導入の統一viewsメトリクス検証",
        "account_info": {
            "page_name": yamasa_account.get('name'),
            "page_id": yamasa_account.get('id'),
            "ig_account_id": yamasa_account.get('instagram_business_account', {}).get('id', '')
        },
        "views_test_results": []
    }
    
    client = InstagramAPIClient()
    
    page_token = yamasa_account.get('access_token', '')
    ig_account_id = results["account_info"]["ig_account_id"]
    
    print(f"🔍 ヤマサリノベアカウント詳細:")
    print(f"   📄 Page ID: {results['account_info']['page_id']}")
    print(f"   📸 IG Account ID: {ig_account_id}")
    print()
    
    if not ig_account_id or not page_token:
        print(f"❌ エラー: Instagram Account IDまたはTokenが不足")
        return False
    
    # Get VIDEO posts (we know from previous test there are 17 in first 25 posts)
    print(f"🔍 ステップ1: VIDEO投稿を取得中...")
    
    try:
        media_params = {
            'fields': 'id,media_type,timestamp,caption',
            'limit': 25,  # We know first page has 17 VIDEOs
            'access_token': page_token
        }
        
        media_response = client.graph_api_request(f'/{ig_account_id}/media', params=media_params)
        
        if not media_response:
            print(f"   ❌ 投稿データの取得に失敗: レスポンスがNone")
            return False
        
        if 'data' not in media_response:
            print(f"   ❌ 投稿データの取得に失敗: dataキーなし")
            print(f"   🔍 レスポンス内容: {media_response}")
            return False
        
        all_media = media_response['data']
        video_media = [media for media in all_media if media.get('media_type') == 'VIDEO']
        
        print(f"   ✅ 投稿データ取得完了")
        print(f"      📊 総投稿数: {len(all_media)}")
        print(f"      🎬 VIDEO投稿数: {len(video_media)}")
        print()
        
        if len(video_media) == 0:
            print(f"⚠️ VIDEO投稿が見つかりませんでした")
            return False
        
        print(f"🧪 ステップ2: viewsメトリクス検証開始...")
        print(f"   📝 検証対象: 最初の5件のVIDEO投稿")
        print()
        
        # Test views metric on first 5 videos
        test_count = min(5, len(video_media))
        views_results = []
        
        for idx, video in enumerate(video_media[:test_count]):
            video_id = video.get('id')
            timestamp = video.get('timestamp')
            caption = video.get('caption', '')[:50] + '...' if video.get('caption') else 'キャプションなし'
            
            print(f"   🎬 VIDEO投稿{idx+1}/5: {video_id[:15]}...")
            print(f"      📅 投稿日: {timestamp}")
            print(f"      💬 キャプション: {caption}")
            
            video_result = {
                "video_id": video_id,
                "timestamp": timestamp,
                "caption": caption,
                "metrics": {}
            }
            
            # Test 1: New views metric
            print(f"      📊 新メトリクス: views取得...")
            try:
                views_params = {
                    'metric': 'views',
                    'access_token': page_token
                }
                
                views_response = client.graph_api_request(f'/{video_id}/insights', params=views_params)
                
                if views_response and 'data' in views_response:
                    views_data = views_response['data']
                    if views_data and len(views_data) > 0:
                        views_value = views_data[0].get('values', [{}])[0].get('value', 0)
                        video_result["metrics"]["views"] = {
                            "success": True,
                            "value": views_value,
                            "raw_data": views_data[0]
                        }
                        print(f"         ✅ Views: {views_value:,} 回")
                    else:
                        video_result["metrics"]["views"] = {
                            "success": False,
                            "error": "Empty data array"
                        }
                        print(f"         ❌ Views: データが空")
                else:
                    video_result["metrics"]["views"] = {
                        "success": False,
                        "error": "No response or missing data key"
                    }
                    print(f"         ❌ Views: レスポンスなし")
                    
            except Exception as e:
                video_result["metrics"]["views"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"         ❌ Views: 例外 - {e}")
            
            # Test 2: Reach for comparison (we know this works)
            print(f"      📊 比較メトリクス: reach取得...")
            try:
                reach_params = {
                    'metric': 'reach',
                    'access_token': page_token
                }
                
                reach_response = client.graph_api_request(f'/{video_id}/insights', params=reach_params)
                
                if reach_response and 'data' in reach_response:
                    reach_data = reach_response['data']
                    if reach_data and len(reach_data) > 0:
                        reach_value = reach_data[0].get('values', [{}])[0].get('value', 0)
                        video_result["metrics"]["reach"] = {
                            "success": True,
                            "value": reach_value
                        }
                        print(f"         ✅ Reach: {reach_value:,} ユーザー")
                    else:
                        video_result["metrics"]["reach"] = {
                            "success": False,
                            "error": "Empty data array"
                        }
                        print(f"         ❌ Reach: データが空")
            except Exception as e:
                video_result["metrics"]["reach"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"         ❌ Reach: 例外 - {e}")
            
            # Test 3: Try old video_views for comparison (expected to fail)
            print(f"      📊 旧メトリクス: video_views取得（失敗予想）...")
            try:
                old_params = {
                    'metric': 'video_views',
                    'access_token': page_token
                }
                
                old_response = client.graph_api_request(f'/{video_id}/insights', params=old_params)
                
                if old_response and 'data' in old_response:
                    old_data = old_response['data']
                    if old_data and len(old_data) > 0:
                        old_value = old_data[0].get('values', [{}])[0].get('value', 0)
                        video_result["metrics"]["video_views_old"] = {
                            "success": True,
                            "value": old_value
                        }
                        print(f"         ⚠️ Video_views（旧）: {old_value:,} 回 - 意外にも取得成功")
                    else:
                        video_result["metrics"]["video_views_old"] = {
                            "success": False,
                            "error": "Empty data array"
                        }
                        print(f"         ❌ Video_views（旧）: データが空")
                else:
                    video_result["metrics"]["video_views_old"] = {
                        "success": False,
                        "error": "No response or missing data key"
                    }
                    print(f"         ❌ Video_views（旧）: レスポンスなし（予想通り）")
                    
            except Exception as e:
                video_result["metrics"]["video_views_old"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"         ❌ Video_views（旧）: 例外 - {e}")
            
            views_results.append(video_result)
            print()
        
        # Create test result
        successful_views = sum(1 for result in views_results 
                             if result.get("metrics", {}).get("views", {}).get("success"))
        successful_reach = sum(1 for result in views_results 
                             if result.get("metrics", {}).get("reach", {}).get("success"))
        
        test_result = {
            "test_name": "views_metric_validation",
            "success": successful_views > 0,
            "data": {
                "videos_tested": len(views_results),
                "successful_views": successful_views,
                "successful_reach": successful_reach,
                "video_results": views_results
            },
            "notes": f"{successful_views}件のVIDEO投稿でviews メトリクス取得成功"
        }
        
    except Exception as e:
        test_result = {
            "test_name": "views_metric_validation",
            "success": False,
            "error": str(e),
            "notes": "views メトリクス検証で例外発生"
        }
        print(f"❌ 例外: {e}")
    
    results["views_test_results"] = [test_result]
    
    # Save results
    output_file = os.path.join(os.path.dirname(__file__), '03-output-data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 結果保存: {output_file}")
    
    # Summary
    if test_result.get("success"):
        successful_views = test_result["data"]["successful_views"]
        successful_reach = test_result["data"]["successful_reach"]
        total_tested = test_result["data"]["videos_tested"]
        
        print(f"\n🏁 検証完了 - 実行結果サマリー")
        print(f"🧪 テストしたVIDEO投稿: {total_tested}件")
        print(f"✅ Views メトリクス取得成功: {successful_views}件")
        print(f"✅ Reach メトリクス取得成功: {successful_reach}件")
        
        if successful_views > 0:
            print("🎉 新しいviews メトリクスの取得に成功しました！")
            print("🔍 結果: 2025年4月の統一メトリクスが正常に機能しています")
            print("🎯 次のステップ: 投稿分析ページでviews データを活用できます")
        else:
            print("⚠️ Views メトリクスは取得できませんでしたが、Reachは正常です")
        
        return True
    else:
        print(f"\n🏁 検証完了 - 実行結果サマリー")
        print("❌ Views メトリクスの検証に失敗しました")
        print("🔧 対策: APIバージョンまたはメトリクス名を再確認する必要があります")
        return False

if __name__ == "__main__":
    success = test_views_metric()
    sys.exit(0 if success else 1)