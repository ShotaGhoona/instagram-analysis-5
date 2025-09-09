#!/usr/bin/env python3
"""
Page Access Token Long-lived Conversion Script

Convert short-lived Page Access Tokens to long-lived Page Access Tokens
for stable Instagram Business Account access.
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.api_client import InstagramAPIClient

def convert_page_tokens_to_long_lived():
    """Convert short-lived Page Access Tokens to long-lived Page Access Tokens"""
    
    print("🚀 Page Access Token長期化変換を開始します")
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
    
    print(f"🔍 処理対象: {len(accounts_data)}件のPage Access Token")
    print("   📝 注: 全てのアカウントを処理します")
    print()
    
    # Results structure
    results = {
        "endpoint": "/oauth/access_token (Page Long-lived)",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "Page Access Token長期化変換テスト",
        "token_conversions": []
    }
    
    # Process all accounts
    sample_count = len(accounts_data)
    
    # Get necessary credentials for token exchange
    app_id = os.getenv('INSTAGRAM_APP_ID')
    app_secret = os.getenv('INSTAGRAM_APP_SECRET')
    
    if not app_id or not app_secret:
        print("❌ エラー: INSTAGRAM_APP_ID または INSTAGRAM_APP_SECRET が設定されていません")
        print("   🔧 対策: .env ファイルに両方の値を設定してください")
        return False
    
    for i in range(sample_count):
        account = accounts_data[i]
        page_name = account.get('name', 'Unknown')
        page_id = account.get('id', 'Unknown')
        ig_account_id = account.get('instagram_business_account', {}).get('id', '')
        page_token = account.get('access_token', '')
        
        print(f"🔍 処理中: {page_name}")
        print(f"   📄 Page ID: {page_id}")
        print(f"   📸 IG Account ID: {ig_account_id}")
        
        if not page_token or not ig_account_id:
            print(f"⚠️ 警告: 必要なトークンまたはIDが不足しています")
            continue
        
        conversion_result = {
            "page_name": page_name,
            "page_id": page_id,
            "ig_account_id": ig_account_id,
            "conversion_attempts": []
        }
        
        # Method 1: Try fb_exchange_token (Facebook Graph API)
        print(f"   🔄 方法1: fb_exchange_token でPage Access Token長期化を試行...")
        try:
            exchange_url = "https://graph.facebook.com/v23.0/oauth/access_token"
            exchange_params = {
                'grant_type': 'fb_exchange_token',
                'client_id': app_id,
                'client_secret': app_secret,
                'fb_exchange_token': page_token
            }
            
            response = requests.get(exchange_url, params=exchange_params)
            
            if response.status_code == 200:
                token_data = response.json()
                
                attempt_result = {
                    "method": "fb_exchange_token",
                    "success": True,
                    "data": token_data,
                    "notes": "Page Access Token長期化変換成功"
                }
                
                expires_in = token_data.get('expires_in', 0)
                new_token = token_data.get('access_token', '')
                
                # Convert seconds to days
                expires_days = expires_in // 86400 if expires_in > 0 else 0
                
                print(f"   ✅ 成功: Page Access Tokenを長期化しました")
                print(f"      🔑 新トークン: {new_token[:50]}...")
                print(f"      ⏰ 有効期限: {expires_days}日間 (約{expires_days//30}ヶ月)")
                
                conversion_result["page_long_lived_token"] = {
                    "token": new_token,
                    "expires_in": expires_in,
                    "expires_days": expires_days,
                    "generated_at": datetime.now().isoformat()
                }
                
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                attempt_result = {
                    "method": "fb_exchange_token",
                    "success": False,
                    "error": error_data,
                    "status_code": response.status_code,
                    "notes": "fb_exchange_token方式でのトークン変換失敗"
                }
                
                print(f"   ❌ 失敗: fb_exchange_token方式")
                print(f"      🔍 ステータス: {response.status_code}")
                print(f"      🔍 エラー: {error_data.get('error', {}).get('message', 'Unknown error')}")
        
        except Exception as e:
            attempt_result = {
                "method": "fb_exchange_token",
                "success": False,
                "error": str(e),
                "notes": "fb_exchange_token方式で例外発生"
            }
            print(f"   ❌ 例外: {e}")
        
        conversion_result["conversion_attempts"].append(attempt_result)
        results["token_conversions"].append(conversion_result)
        
        print()
    
    # Save results
    output_file = os.path.join(os.path.dirname(__file__), '01-output-data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 結果保存: {output_file}")
    
    # Summary
    total_accounts = len(results["token_conversions"])
    successful_conversions = 0
    
    for conversion in results["token_conversions"]:
        if conversion.get("page_long_lived_token"):
            successful_conversions += 1
    
    print(f"\n🏁 変換完了 - 実行結果サマリー")
    print(f"📊 総アカウント数: {total_accounts}")
    print(f"✅ 成功した変換: {successful_conversions}")
    print(f"❌ 失敗した変換: {total_accounts - successful_conversions}")
    
    if successful_conversions > 0:
        print("🎉 Page Access Tokenの長期化に成功しました！")
        print("🔍 次のステップ: 新しい長期トークンでInstagramデータ取得の安定運用が可能です")
        return True
    else:
        print("⚠️ Page Access Tokenの長期化に失敗しました")
        print("🔧 対策: アプリの設定とINSTAGRAM_APP_ID、INSTAGRAM_APP_SECRETを確認してください")
        return False

if __name__ == "__main__":
    success = convert_page_tokens_to_long_lived()
    sys.exit(0 if success else 1)