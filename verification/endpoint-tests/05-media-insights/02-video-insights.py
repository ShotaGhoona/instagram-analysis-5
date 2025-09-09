#!/usr/bin/env python3
"""
Video Insights Verification Script

Extended search for VIDEO posts (Reels) from ヤマサリノベ account
and test video_views metric on actual video content.
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.api_client import InstagramAPIClient

def test_video_insights():
    """Test video insights with extended search for VIDEO posts"""
    
    print("🚀 Video Insights (Reels) 検証を開始します")
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
    
    # Find 有限会社カネタケ account specifically
    kanetake_account = None
    for account in accounts_data:
        if account.get('name') == 'ヤマサリノベ':
            kanetake_account = account
            break
    
    if not kanetake_account:
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
            kanetake_account['access_token'] = yamasa_token
        else:
            print(f"⚠️ 長期トークンが見つからず、既存トークンを使用")
            
    except FileNotFoundError:
        print(f"⚠️ 長期トークンファイルなし、既存トークンを使用")
    
    print(f"🎯 検証対象: ヤマサリノベ専用 - VIDEO投稿（Reels）探索")
    print("   📝 注: より多くの投稿データを遡ってVIDEO投稿を検索します")
    print()
    
    # Results structure
    results = {
        "endpoint": "/{ig-media-id}/insights?metric=video_views (Video Focus)",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "Reels（VIDEO投稿）の動画視聴数メトリクス検証",
        "account_info": {
            "page_name": kanetake_account.get('name'),
            "page_id": kanetake_account.get('id'),
            "ig_account_id": kanetake_account.get('instagram_business_account', {}).get('id', '')
        },
        "video_search_results": []
    }
    
    client = InstagramAPIClient()
    
    page_token = kanetake_account.get('access_token', '')
    ig_account_id = results["account_info"]["ig_account_id"]
    
    print(f"🔍 ヤマサリノベアカウント詳細:")
    print(f"   📄 Page ID: {results['account_info']['page_id']}")
    print(f"   📸 IG Account ID: {ig_account_id}")
    print()
    
    if not ig_account_id or not page_token:
        print(f"❌ エラー: Instagram Account IDまたはTokenが不足")
        return False
    
    # Extended media search with pagination
    print(f"🔍 ステップ1: 拡張投稿検索を開始（VIDEO投稿を探索中）...")
    
    all_media = []
    video_media = []
    next_url = None
    page_count = 0
    max_pages = 10  # Maximum 10 pages to search through
    
    try:
        while page_count < max_pages:
            page_count += 1
            print(f"   📄 ページ{page_count}: 投稿データ取得中...")
            
            if next_url:
                # Use pagination URL
                response = requests.get(next_url)
                if response.status_code != 200:
                    break
                media_response = response.json()
            else:
                # First page request
                media_params = {
                    'fields': 'id,media_type,timestamp,caption',
                    'limit': 25,  # Get 25 posts per page
                    'access_token': page_token
                }
                media_response = client.graph_api_request(f'/{ig_account_id}/media', params=media_params)
            
            if not media_response or 'data' not in media_response:
                print(f"   ⚠️ ページ{page_count}: データなし、検索終了")
                break
            
            page_media = media_response['data']
            all_media.extend(page_media)
            
            # Filter for VIDEO posts
            page_videos = [media for media in page_media if media.get('media_type') == 'VIDEO']
            video_media.extend(page_videos)
            
            print(f"   📊 ページ{page_count}: {len(page_media)}件取得 (VIDEO: {len(page_videos)}件)")
            
            # Check for more pages
            paging = media_response.get('paging', {})
            next_url = paging.get('next')
            
            if not next_url:
                print(f"   ✅ 全ページ検索完了")
                break
            
            # If we found videos, we can test with fewer pages
            if len(video_media) >= 3:
                print(f"   🎯 十分なVIDEO投稿を発見、検索を効率化")
                break
        
        print(f"\n📊 検索結果サマリー:")
        print(f"   📄 検索ページ数: {page_count}")
        print(f"   📸 総投稿数: {len(all_media)}")
        print(f"   🎬 VIDEO投稿数: {len(video_media)}")
        
        # Test insights on found videos
        if len(video_media) == 0:
            print(f"\n⚠️ VIDEO投稿が見つかりませんでした")
            print(f"   📝 検索した{len(all_media)}件の投稿は全て非VIDEO形式")
            
            # Show media type distribution
            type_counts = {}
            for media in all_media:
                media_type = media.get('media_type', 'UNKNOWN')
                type_counts[media_type] = type_counts.get(media_type, 0) + 1
            
            print(f"   📊 投稿タイプ分布:")
            for media_type, count in type_counts.items():
                print(f"      {media_type}: {count}件")
            
            test_result = {
                "test_name": "video_insights",
                "success": False,
                "error": "No VIDEO posts found in search",
                "search_stats": {
                    "pages_searched": page_count,
                    "total_media": len(all_media),
                    "video_media": len(video_media),
                    "media_type_distribution": type_counts
                },
                "notes": "拡張検索でもVIDEO投稿が見つからず"
            }
            
        else:
            print(f"\n🎉 {len(video_media)}件のVIDEO投稿を発見!")
            print(f"   🧪 動画視聴数インサイト検証を開始...")
            
            video_insights_results = []
            
            # Test video insights for each found video
            test_count = min(3, len(video_media))  # Test up to 3 videos
            
            for idx, video in enumerate(video_media[:test_count]):
                video_id = video.get('id')
                timestamp = video.get('timestamp')
                caption = video.get('caption', '')[:50] + '...' if video.get('caption') else 'キャプションなし'
                
                print(f"\n   🎬 VIDEO投稿{idx+1}: {video_id[:15]}...")
                print(f"      📅 投稿日: {timestamp}")
                print(f"      💬 キャプション: {caption}")
                
                video_insight = {
                    "video_id": video_id,
                    "timestamp": timestamp,
                    "caption": caption,
                    "insights": {}
                }
                
                # Test video_views metric
                print(f"      📊 テスト: 動画視聴数取得...")
                try:
                    video_params = {
                        'metric': 'video_views',
                        'access_token': page_token
                    }
                    
                    video_response = client.graph_api_request(f'/{video_id}/insights', params=video_params)
                    
                    if video_response and 'data' in video_response:
                        video_data = video_response['data']
                        if video_data and len(video_data) > 0:
                            video_value = video_data[0].get('values', [{}])[0].get('value', 0)
                            video_insight["insights"]["video_views"] = {
                                "success": True,
                                "value": video_value,
                                "raw_data": video_data[0]
                            }
                            print(f"         ✅ 動画視聴数: {video_value:,} 回")
                        else:
                            video_insight["insights"]["video_views"] = {
                                "success": False,
                                "error": "Empty data array"
                            }
                            print(f"         ❌ 動画視聴数: データが空")
                    else:
                        video_insight["insights"]["video_views"] = {
                            "success": False,
                            "error": "No response or missing data key"
                        }
                        print(f"         ❌ 動画視聴数: レスポンスなし")
                        
                except Exception as e:
                    video_insight["insights"]["video_views"] = {
                        "success": False,
                        "error": str(e)
                    }
                    print(f"         ❌ 動画視聴数: 例外 - {e}")
                
                # Also test reach for comparison
                print(f"      📊 比較テスト: リーチ取得...")
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
                            video_insight["insights"]["reach"] = {
                                "success": True,
                                "value": reach_value
                            }
                            print(f"         ✅ リーチ: {reach_value:,} ユーザー")
                        else:
                            video_insight["insights"]["reach"] = {
                                "success": False,
                                "error": "Empty data array"
                            }
                            print(f"         ❌ リーチ: データが空")
                except Exception as e:
                    video_insight["insights"]["reach"] = {
                        "success": False,
                        "error": str(e)
                    }
                    print(f"         ❌ リーチ: 例外 - {e}")
                
                video_insights_results.append(video_insight)
            
            # Create success test result
            successful_video_views = sum(1 for result in video_insights_results 
                                       if result.get("insights", {}).get("video_views", {}).get("success"))
            
            test_result = {
                "test_name": "video_insights",
                "success": successful_video_views > 0,
                "data": {
                    "videos_found": len(video_media),
                    "videos_tested": len(video_insights_results),
                    "successful_video_views": successful_video_views,
                    "video_insights": video_insights_results
                },
                "search_stats": {
                    "pages_searched": page_count,
                    "total_media": len(all_media),
                    "video_media": len(video_media)
                },
                "notes": f"{successful_video_views}件のVIDEO投稿で動画視聴数取得成功"
            }
        
    except Exception as e:
        test_result = {
            "test_name": "video_insights",
            "success": False,
            "error": str(e),
            "notes": "VIDEO投稿検索で例外発生"
        }
        print(f"❌ 例外: {e}")
    
    results["video_search_results"] = [test_result]
    
    # Save results
    output_file = os.path.join(os.path.dirname(__file__), '02-output-data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 結果保存: {output_file}")
    
    # Summary
    if test_result.get("success"):
        successful_videos = test_result["data"]["successful_video_views"]
        total_videos = test_result["data"]["videos_tested"]
        
        print(f"\n🏁 検証完了 - 実行結果サマリー")
        print(f"🔍 検索ページ数: {test_result['search_stats']['pages_searched']}")
        print(f"📸 総投稿数: {test_result['search_stats']['total_media']}")
        print(f"🎬 発見したVIDEO投稿: {test_result['search_stats']['video_media']}件")
        print(f"🧪 テストしたVIDEO投稿: {total_videos}件")
        print(f"✅ 動画視聴数取得成功: {successful_videos}件")
        
        print("🎉 VIDEO投稿の動画視聴数取得に成功しました！")
        print("🔍 次のステップ: 投稿分析ページでVIDEO投稿の視聴数データを活用できます")
        return True
    else:
        print(f"\n🏁 検証完了 - 実行結果サマリー")
        if "search_stats" in test_result:
            print(f"🔍 検索ページ数: {test_result['search_stats']['pages_searched']}")
            print(f"📸 総投稿数: {test_result['search_stats']['total_media']}")
            print(f"🎬 発見したVIDEO投稿: {test_result['search_stats']['video_media']}件")
        
        print("⚠️ VIDEO投稿が見つからず、動画視聴数の検証ができませんでした")
        print("🔧 対策: 他のアカウントまたはより長期間のデータ検索が必要です")
        return False

if __name__ == "__main__":
    success = test_video_insights()
    sys.exit(0 if success else 1)