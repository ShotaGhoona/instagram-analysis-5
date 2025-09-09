#!/usr/bin/env python3
"""
Instagram Long-lived Token Generation Script

Convert Page Access Tokens to Instagram-specific long-lived tokens
for accessing Instagram insights and detailed analytics data.
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.api_client import InstagramAPIClient

def generate_ig_long_lived_tokens():
    """Generate Instagram-specific long-lived tokens from Page Access Tokens"""
    
    print("🚀 Instagram専用長期トークン生成を開始します")
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
    print("   📝 注: 最初の3件をサンプルとして処理します")
    print()
    
    # Results structure
    results = {
        "endpoint": "/access_token (Instagram Long-lived)",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "Instagram専用長期トークン生成テスト",
        "token_conversions": []
    }
    
    # Process first 3 accounts as sample
    sample_count = min(3, len(accounts_data))
    instagram_app_secret = os.getenv('INSTAGRAM_APP_SECRET')
    
    if not instagram_app_secret:
        print("❌ エラー: INSTAGRAM_APP_SECRET が設定されていません")
        print("   🔧 対策: .env ファイルにINSTAGRAM_APP_SECRETを追加してください")
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
        
        # Method 1: Try ig_exchange_token (Instagram Graph API)
        print(f"   🔄 方法1: ig_exchange_token でトークン変換を試行...")
        try:
            exchange_url = "https://graph.instagram.com/access_token"
            exchange_params = {
                'grant_type': 'ig_exchange_token',
                'client_secret': instagram_app_secret,
                'access_token': page_token
            }
            
            response = requests.post(exchange_url, params=exchange_params)
            
            if response.status_code == 200:
                token_data = response.json()
                
                attempt_result = {
                    "method": "ig_exchange_token",
                    "success": True,
                    "data": token_data,
                    "notes": "Instagram専用長期トークン生成成功"
                }
                
                expires_in = token_data.get('expires_in', 0)
                new_token = token_data.get('access_token', '')
                
                # Convert seconds to days
                expires_days = expires_in // 86400 if expires_in > 0 else 0
                
                print(f"   ✅ 成功: Instagram専用トークンを生成しました")
                print(f"      🔑 新トークン: {new_token[:50]}...")
                print(f"      ⏰ 有効期限: {expires_days}日間")
                
                conversion_result["ig_long_lived_token"] = {
                    "token": new_token,
                    "expires_in": expires_in,
                    "expires_days": expires_days,
                    "generated_at": datetime.now().isoformat()
                }
                
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                attempt_result = {
                    "method": "ig_exchange_token",
                    "success": False,
                    "error": error_data,
                    "status_code": response.status_code,
                    "notes": "ig_exchange_token方式でのトークン変換失敗"
                }
                
                print(f"   ❌ 失敗: ig_exchange_token方式")
                print(f"      🔍 ステータス: {response.status_code}")
                print(f"      🔍 エラー: {error_data.get('error', {}).get('message', 'Unknown error')}")
        
        except Exception as e:
            attempt_result = {
                "method": "ig_exchange_token",
                "success": False,
                "error": str(e),
                "notes": "ig_exchange_token方式で例外発生"
            }
            print(f"   ❌ 例外: {e}")
        
        conversion_result["conversion_attempts"].append(attempt_result)
        
        # Method 2: Try ig_refresh_token (if we have an IG token already)
        print(f"   🔄 方法2: ig_refresh_token でトークン更新を試行...")
        try:
            refresh_url = "https://graph.instagram.com/refresh_access_token"
            refresh_params = {
                'grant_type': 'ig_refresh_token',
                'access_token': page_token
            }
            
            response = requests.get(refresh_url, params=refresh_params)
            
            if response.status_code == 200:
                refresh_data = response.json()
                
                attempt_result = {
                    "method": "ig_refresh_token",
                    "success": True,
                    "data": refresh_data,
                    "notes": "ig_refresh_token方式でトークン更新成功"
                }
                
                print(f"   ✅ 成功: ig_refresh_token方式でトークン更新")
                
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                attempt_result = {
                    "method": "ig_refresh_token",
                    "success": False,
                    "error": error_data,
                    "status_code": response.status_code,
                    "notes": "ig_refresh_token方式でのトークン更新失敗（想定内）"
                }
                
                print(f"   ⚠️ 失敗: ig_refresh_token方式（想定内）")
                print(f"      🔍 理由: Page Access TokenはInstagram専用トークンではない")
        
        except Exception as e:
            attempt_result = {
                "method": "ig_refresh_token",
                "success": False,
                "error": str(e),
                "notes": "ig_refresh_token方式で例外発生"
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
        for attempt in conversion.get("conversion_attempts", []):
            if attempt.get("success"):
                successful_conversions += 1
                break
    
    print(f"\n🏁 変換完了 - 実行結果サマリー")
    print(f"📊 総アカウント数: {total_accounts}")
    print(f"✅ 成功した変換: {successful_conversions}")
    print(f"❌ 失敗した変換: {total_accounts - successful_conversions}")
    
    if successful_conversions > 0:
        print("🎉 Instagram専用長期トークンの生成に成功しました！")
        print("🔍 次のステップ: 新しいトークンでインサイトデータ取得テストが可能です")
        return True
    else:
        print("⚠️ Instagram専用トークンの生成に失敗しました")
        print("🔧 対策: アプリの設定とINSTAGRAM_APP_SECRETを確認してください")
        return False

if __name__ == "__main__":
    success = generate_ig_long_lived_tokens()
    sys.exit(0 if success else 1)