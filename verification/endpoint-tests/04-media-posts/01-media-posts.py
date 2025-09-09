#!/usr/bin/env python3
"""
Media Posts Verification Script

Test GET /{ig-user-id}/media?fields=id,timestamp,media_type,caption,like_count,comments_count,media_url,thumbnail_url,permalink&limit=25
for daily media posts data collection.
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.api_client import InstagramAPIClient

def test_media_posts():
    """Test media posts retrieval for daily posts data collection"""
    
    print("🚀 Media Posts 検証を開始します")
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
    print("   📝 注: 最初の3件をサンプルとしてメディア投稿データを取得します")
    print()
    
    # Results structure
    results = {
        "endpoint": "/{ig-user-id}/media (Media Posts)",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "毎日収集用投稿データ取得テスト",
        "account_tests": []
    }
    
    client = InstagramAPIClient()
    
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
    
    # Process first 3 accounts as sample
    sample_count = min(3, len(accounts_data))
    
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
        
        # Test 1: Full media posts retrieval
        print(f"   🧪 テスト1: 投稿データ一括取得...")
        try:
            media_params = {
                'fields': 'id,timestamp,media_type,caption,like_count,comments_count,media_url,thumbnail_url,permalink',
                'limit': 10,  # Limit to 10 for testing
                'access_token': page_token
            }
            
            response = client.graph_api_request(f'/{ig_account_id}/media', params=media_params)
            
            if response and 'data' in response:
                media_list = response['data']
                test_result = {
                    "test_name": "full_media_posts",
                    "success": True,
                    "data": response,
                    "notes": "投稿データ一括取得成功"
                }
                
                print(f"   ✅ 成功: {len(media_list)}件の投稿データを取得しました")
                
                # Display sample data for first few posts
                for idx, media in enumerate(media_list[:3]):
                    print(f"      📸 投稿{idx+1}:")
                    print(f"         🆔 Media ID: {media.get('id', 'N/A')}")
                    print(f"         📅 投稿日時: {media.get('timestamp', 'N/A')}")
                    print(f"         🎭 タイプ: {media.get('media_type', 'N/A')}")
                    print(f"         💬 キャプション: {(media.get('caption', 'N/A') or 'なし')[:30]}...")
                    print(f"         👍 いいね数: {media.get('like_count', 'N/A'):,}")
                    print(f"         💭 コメント数: {media.get('comments_count', 'N/A'):,}")
                    print(f"         🖼️  メディアURL: {'取得済み' if media.get('media_url') else 'N/A'}")
                    print(f"         🔗 パーマリンク: {'取得済み' if media.get('permalink') else 'N/A'}")
                
                if len(media_list) > 3:
                    print(f"      📋 他{len(media_list)-3}件の投稿データも取得済み")
                
            else:
                test_result = {
                    "test_name": "full_media_posts",
                    "success": False,
                    "error": "API response is None or missing data",
                    "notes": "投稿データ一括取得失敗"
                }
                print(f"   ❌ 失敗: 投稿データの取得に失敗")
                
        except Exception as e:
            test_result = {
                "test_name": "full_media_posts",
                "success": False,
                "error": str(e),
                "notes": "投稿データ一括取得で例外発生"
            }
            print(f"   ❌ 例外: {e}")
        
        account_result["tests"].append(test_result)
        
        # Test 2: Individual field validation (if we have media)
        if test_result.get("success") and test_result.get("data", {}).get("data"):
            print(f"   🧪 テスト2: 個別フィールド検証...")
            try:
                sample_media_id = test_result["data"]["data"][0]["id"]
                individual_fields = ['id', 'timestamp', 'media_type', 'caption', 'like_count', 'comments_count', 'media_url', 'permalink']
                field_results = {}
                
                for field in individual_fields:
                    field_params = {
                        'fields': field,
                        'limit': 1,
                        'access_token': page_token
                    }
                    
                    field_response = client.graph_api_request(f'/{ig_account_id}/media', params=field_params)
                    if field_response and 'data' in field_response and len(field_response['data']) > 0:
                        first_media = field_response['data'][0]
                        if field in first_media:
                            field_results[field] = {
                                "available": True,
                                "value": first_media[field]
                            }
                            # Format different field types appropriately
                            if field in ['like_count', 'comments_count']:
                                print(f"      ✅ {field}: {first_media[field]:,}")
                            elif field in ['media_url', 'permalink']:
                                print(f"      ✅ {field}: URL取得済み")
                            elif field == 'caption':
                                caption_preview = (first_media[field] or 'なし')[:20]
                                print(f"      ✅ {field}: {caption_preview}...")
                            else:
                                print(f"      ✅ {field}: {first_media[field]}")
                        else:
                            field_results[field] = {
                                "available": False,
                                "value": None
                            }
                            print(f"      ❌ {field}: フィールドが利用できません")
                    else:
                        field_results[field] = {
                            "available": False,
                            "value": None
                        }
                        print(f"      ❌ {field}: フィールドが利用できません")
                
                test_result = {
                    "test_name": "individual_fields",
                    "success": True,
                    "data": field_results,
                    "notes": "個別フィールド検証完了"
                }
                
            except Exception as e:
                test_result = {
                    "test_name": "individual_fields", 
                    "success": False,
                    "error": str(e),
                    "notes": "個別フィールド検証で例外発生"
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
    total_media_retrieved = 0
    
    for account in results["account_tests"]:
        for test in account.get("tests", []):
            if test.get("test_name") == "full_media_posts" and test.get("success"):
                successful_accounts += 1
                if test.get("data", {}).get("data"):
                    total_media_retrieved += len(test["data"]["data"])
                break
    
    print(f"\n🏁 検証完了 - 実行結果サマリー")
    print(f"📊 総アカウント数: {total_accounts}")
    print(f"✅ 成功したアカウント: {successful_accounts}")
    print(f"❌ 失敗したアカウント: {total_accounts - successful_accounts}")
    print(f"📸 取得した投稿総数: {total_media_retrieved}件")
    
    if successful_accounts > 0:
        print("🎉 投稿データの取得に成功しました！")
        print("🔍 次のステップ: 毎日のデータ収集で投稿情報を定期取得できます")
        return True
    else:
        print("⚠️ 投稿データの取得に失敗しました")
        print("🔧 対策: Page Access Tokenとinstagram_business_accountの設定を確認してください")
        return False

if __name__ == "__main__":
    success = test_media_posts()
    sys.exit(0 if success else 1)