#!/usr/bin/env python3
"""
Account Basic Info Verification Script

Test GET /{ig-user-id}?fields=followers_count,follows_count,media_count
for daily account stats collection.
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.api_client import InstagramAPIClient

def test_account_basic_info():
    """Test account basic info retrieval for daily stats collection"""
    
    print("🚀 Account Basic Info 検証を開始します")
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
    print("   📝 注: 全アカウントの基本情報を取得します")
    print()
    
    # Results structure
    results = {
        "endpoint": "/{ig-user-id} (Account Basic Info)",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "毎日収集用アカウント基本情報テスト",
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
    
    for i, account in enumerate(accounts_data):
        page_name = account.get('name', 'Unknown')
        page_id = account.get('id', 'Unknown')
        ig_account_id = account.get('instagram_business_account', {}).get('id', '')
        page_token = account.get('access_token', '')
        
        print(f"🔍 テスト {i+1}/{len(accounts_data)}: {page_name}")
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
        
        # Test 1: Basic account info (followers, follows, media count + profile info)
        print(f"   🧪 テスト1: アカウント基本情報取得...")
        try:
            basic_info_params = {
                'fields': 'id,username,name,profile_picture_url,followers_count,follows_count,media_count',
                'access_token': page_token
            }
            
            response = client.graph_api_request(f'/{ig_account_id}', params=basic_info_params)
            
            if response:
                test_result = {
                    "test_name": "basic_account_info",
                    "success": True,
                    "data": response,
                    "notes": "アカウント基本情報取得成功"
                }
                
                print(f"   ✅ 成功: アカウント基本情報を取得しました")
                print(f"      👤 ユーザー名: @{response.get('username', 'N/A')}")
                print(f"      📛 表示名: {response.get('name', 'N/A')}")
                print(f"      👥 フォロワー数: {response.get('followers_count', 'N/A'):,}")
                print(f"      ➡️  フォロー数: {response.get('follows_count', 'N/A'):,}")
                print(f"      📸 投稿数: {response.get('media_count', 'N/A'):,}")
                print(f"      🖼️  プロフィール画像: {'取得済み' if response.get('profile_picture_url') else 'N/A'}")
                
            else:
                test_result = {
                    "test_name": "basic_account_info",
                    "success": False,
                    "error": "API response is None",
                    "notes": "アカウント基本情報取得失敗"
                }
                print(f"   ❌ 失敗: アカウント基本情報の取得に失敗")
                
        except Exception as e:
            test_result = {
                "test_name": "basic_account_info",
                "success": False,
                "error": str(e),
                "notes": "アカウント基本情報取得で例外発生"
            }
            print(f"   ❌ 例外: {e}")
        
        account_result["tests"].append(test_result)
        
        # Test 2: Individual field validation
        print(f"   🧪 テスト2: 個別フィールド検証...")
        try:
            # Test each field individually to confirm availability
            individual_fields = ['followers_count', 'follows_count', 'media_count', 'name', 'username', 'profile_picture_url']
            field_results = {}
            
            for field in individual_fields:
                field_params = {
                    'fields': field,
                    'access_token': page_token
                }
                
                field_response = client.graph_api_request(f'/{ig_account_id}', params=field_params)
                if field_response and field in field_response:
                    field_results[field] = {
                        "available": True,
                        "value": field_response[field]
                    }
                    # Format numeric fields with commas, others as-is
                    if field in ['followers_count', 'follows_count', 'media_count']:
                        print(f"      ✅ {field}: {field_response[field]:,}")
                    elif field == 'profile_picture_url':
                        print(f"      ✅ {field}: URL取得済み")
                    else:
                        print(f"      ✅ {field}: {field_response[field]}")
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
    
    for account in results["account_tests"]:
        for test in account.get("tests", []):
            if test.get("test_name") == "basic_account_info" and test.get("success"):
                successful_accounts += 1
                break
    
    print(f"\n🏁 検証完了 - 実行結果サマリー")
    print(f"📊 総アカウント数: {total_accounts}")
    print(f"✅ 成功したアカウント: {successful_accounts}")
    print(f"❌ 失敗したアカウント: {total_accounts - successful_accounts}")
    
    if successful_accounts > 0:
        print("🎉 アカウント基本情報の取得に成功しました！")
        print("🔍 次のステップ: 毎日のデータ収集でこれらの情報を定期取得できます")
        return True
    else:
        print("⚠️ アカウント基本情報の取得に失敗しました")
        print("🔧 対策: Page Access Tokenとinstagram_business_accountの設定を確認してください")
        return False

if __name__ == "__main__":
    success = test_account_basic_info()
    sys.exit(0 if success else 1)