#!/usr/bin/env python3
"""
Instagram Business Account Token Retrieval Script

Retrieve Instagram Business Account specific access tokens from Facebook Pages.
This is the missing step between Page Access Tokens and Instagram long-lived tokens.
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.api_client import InstagramAPIClient

def get_ig_business_account_tokens():
    """Get Instagram Business Account specific access tokens"""
    
    print("🚀 Instagram Business Account専用トークン取得を開始します")
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
    
    # Extract accounts data and user access token
    accounts_data = None
    user_access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')  # This is the Facebook User Access Token
    
    for test in me_data.get('tests', []):
        if test.get('test_name') == 'user_accounts':
            accounts_data = test.get('data', {}).get('data', [])
            break
    
    if not accounts_data:
        print("❌ エラー: アカウントデータが見つかりません")
        return False
    
    if not user_access_token:
        print("❌ エラー: INSTAGRAM_ACCESS_TOKEN が設定されていません")
        return False
    
    print(f"🔍 処理対象: {len(accounts_data)}件のFacebookページ")
    print("   📝 注: 最初の3件をサンプルとして処理します")
    print()
    
    # Results structure
    results = {
        "endpoint": "Instagram Business Account Token",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "Instagram Business Account専用アクセストークン取得",
        "token_retrievals": []
    }
    
    # Process first 3 accounts as sample
    sample_count = min(3, len(accounts_data))
    
    for i in range(sample_count):
        account = accounts_data[i]
        page_name = account.get('name', 'Unknown')
        page_id = account.get('id', 'Unknown')
        ig_account_id = account.get('instagram_business_account', {}).get('id', '')
        page_token = account.get('access_token', '')
        
        print(f"🔍 処理中: {page_name}")
        print(f"   📄 Facebook Page ID: {page_id}")
        print(f"   📸 Instagram Account ID: {ig_account_id}")
        
        if not page_id or not ig_account_id:
            print(f"⚠️ 警告: 必要なIDが不足しています")
            continue
        
        token_result = {
            "page_name": page_name,
            "page_id": page_id,
            "ig_account_id": ig_account_id,
            "retrieval_attempts": []
        }
        
        # Method 1: Get IG account details with access_token field
        print(f"   🔄 方法1: Instagram Business Account情報とトークン取得...")
        try:
            ig_details_url = f"https://graph.facebook.com/v23.0/{ig_account_id}"
            ig_details_params = {
                'fields': 'id,username,media_count,followers_count,access_token',
                'access_token': page_token  # Use Page Access Token
            }
            
            response = requests.get(ig_details_url, params=ig_details_params)
            
            if response.status_code == 200:
                ig_data = response.json()
                
                attempt_result = {
                    "method": "ig_account_details",
                    "success": True,
                    "data": ig_data,
                    "notes": "Instagram Business Account詳細情報取得成功"
                }
                
                username = ig_data.get('username', 'N/A')
                followers = ig_data.get('followers_count', 'N/A')
                ig_access_token = ig_data.get('access_token', None)
                
                print(f"   ✅ 成功: Instagram Business Account情報を取得")
                print(f"      📱 ユーザー名: @{username}")
                print(f"      👥 フォロワー数: {followers}")
                
                if ig_access_token:
                    print(f"      🔑 IG専用トークン: {ig_access_token[:50]}...")
                    token_result["ig_business_token"] = {
                        "token": ig_access_token,
                        "retrieved_at": datetime.now().isoformat(),
                        "source": "ig_account_details"
                    }
                else:
                    print(f"      ⚠️ 警告: Instagram専用トークンが含まれていません")
                
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                attempt_result = {
                    "method": "ig_account_details",
                    "success": False,
                    "error": error_data,
                    "status_code": response.status_code,
                    "notes": "Instagram Business Account詳細情報取得失敗"
                }
                
                print(f"   ❌ 失敗: Instagram Business Account詳細取得")
                print(f"      🔍 ステータス: {response.status_code}")
                print(f"      🔍 エラー: {error_data.get('error', {}).get('message', 'Unknown error')}")
        
        except Exception as e:
            attempt_result = {
                "method": "ig_account_details",
                "success": False,
                "error": str(e),
                "notes": "Instagram Business Account詳細取得で例外発生"
            }
            print(f"   ❌ 例外: {e}")
        
        token_result["retrieval_attempts"].append(attempt_result)
        
        # Method 2: Try using Facebook Page endpoint to get IG accounts
        print(f"   🔄 方法2: Facebookページ経由でInstagram Business Account取得...")
        try:
            page_ig_url = f"https://graph.facebook.com/v23.0/{page_id}"
            page_ig_params = {
                'fields': 'instagram_business_account{id,username,access_token}',
                'access_token': user_access_token  # Use User Access Token
            }
            
            response = requests.get(page_ig_url, params=page_ig_params)
            
            if response.status_code == 200:
                page_data = response.json()
                
                attempt_result = {
                    "method": "page_ig_account",
                    "success": True,
                    "data": page_data,
                    "notes": "Page経由でInstagram Business Account取得成功"
                }
                
                ig_account_data = page_data.get('instagram_business_account', {})
                if ig_account_data:
                    username = ig_account_data.get('username', 'N/A')
                    ig_access_token = ig_account_data.get('access_token', None)
                    
                    print(f"   ✅ 成功: Page経由でInstagram Business Account取得")
                    print(f"      📱 ユーザー名: @{username}")
                    
                    if ig_access_token and not token_result.get("ig_business_token"):
                        print(f"      🔑 IG専用トークン: {ig_access_token[:50]}...")
                        token_result["ig_business_token"] = {
                            "token": ig_access_token,
                            "retrieved_at": datetime.now().isoformat(),
                            "source": "page_ig_account"
                        }
                    elif ig_access_token:
                        print(f"      🔍 情報: トークンは既に取得済み")
                    else:
                        print(f"      ⚠️ 警告: Instagram専用トークンが含まれていません")
                else:
                    print(f"   ⚠️ 警告: Instagram Business Accountデータが空です")
                
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                attempt_result = {
                    "method": "page_ig_account",
                    "success": False,
                    "error": error_data,
                    "status_code": response.status_code,
                    "notes": "Page経由Instagram Business Account取得失敗"
                }
                
                print(f"   ❌ 失敗: Page経由Instagram Business Account取得")
                print(f"      🔍 ステータス: {response.status_code}")
                print(f"      🔍 エラー: {error_data.get('error', {}).get('message', 'Unknown error')}")
        
        except Exception as e:
            attempt_result = {
                "method": "page_ig_account",
                "success": False,
                "error": str(e),
                "notes": "Page経由Instagram Business Account取得で例外発生"
            }
            print(f"   ❌ 例外: {e}")
        
        token_result["retrieval_attempts"].append(attempt_result)
        results["token_retrievals"].append(token_result)
        
        print()
    
    # Save results
    output_file = os.path.join(os.path.dirname(__file__), '01-output-data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 結果保存: {output_file}")
    
    # Summary
    total_accounts = len(results["token_retrievals"])
    successful_retrievals = 0
    
    for retrieval in results["token_retrievals"]:
        if retrieval.get("ig_business_token"):
            successful_retrievals += 1
    
    print(f"\n🏁 取得完了 - 実行結果サマリー")
    print(f"📊 総アカウント数: {total_accounts}")
    print(f"✅ 成功したトークン取得: {successful_retrievals}")
    print(f"❌ 失敗したトークン取得: {total_accounts - successful_retrievals}")
    
    if successful_retrievals > 0:
        print("🎉 Instagram Business Account専用トークンの取得に成功しました！")
        print("🔍 次のステップ: これらのトークンを長期トークンに変換できます")
        return True
    else:
        print("⚠️ Instagram Business Account専用トークンの取得に失敗しました")
        print("🔧 対策: アプリの権限とInstagram Business Account連携を確認してください")
        return False

if __name__ == "__main__":
    success = get_ig_business_account_tokens()
    sys.exit(0 if success else 1)