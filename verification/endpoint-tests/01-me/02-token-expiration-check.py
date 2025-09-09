#!/usr/bin/env python3
"""
Page Access Token expiration check script

Check the expiration time of Page Access Tokens for Instagram Business Accounts
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.api_client import InstagramAPIClient

def check_token_expiration():
    """Check Page Access Token expiration for Instagram Business Accounts"""
    
    print("🚀 Page Access Token 有効期限確認を開始します")
    print(f"📅 確認実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print()
    
    # Load previous results to get Page Access Tokens
    input_file = os.path.join(os.path.dirname(__file__), '01-output-data.json')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            previous_data = json.load(f)
    except FileNotFoundError:
        print("❌ エラー: 01-output-data.json が見つかりません")
        print("   🔧 対策: 先に 01-basic-user-info.py を実行してください")
        return False
    
    # Extract Instagram accounts from previous results
    instagram_accounts = []
    for test in previous_data.get('tests', []):
        if test.get('test_name') == 'user_accounts' and test.get('success'):
            instagram_accounts = test.get('instagram_accounts', [])
            break
    
    if not instagram_accounts:
        print("❌ エラー: Instagram Business Accounts が見つかりません")
        return False
    
    print(f"🔍 検証対象: {len(instagram_accounts)}件のInstagram Business Account")
    print()
    
    # Results structure
    results = {
        "endpoint": "/debug_token",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "Page Access Token有効期限確認",
        "token_checks": []
    }
    
    # Get Page Access Tokens from accounts data
    accounts_data = None
    for test in previous_data.get('tests', []):
        if test.get('test_name') == 'user_accounts':
            accounts_data = test.get('data', {}).get('data', [])
            break
    
    # Check first 3 tokens as sample
    sample_count = min(3, len(accounts_data)) if accounts_data else 0
    
    for i in range(sample_count):
        account = accounts_data[i]
        page_name = account.get('name', 'Unknown')
        page_id = account.get('id', 'Unknown')
        access_token = account.get('access_token', '')
        
        print(f"🔍 検証中: {page_name} (ID: {page_id})")
        
        if not access_token:
            print(f"⚠️ 警告: アクセストークンが見つかりません")
            continue
        
        try:
            # Check token info using debug_token endpoint
            debug_url = f"https://graph.facebook.com/debug_token"
            params = {
                'input_token': access_token,
                'access_token': os.getenv('INSTAGRAM_ACCESS_TOKEN')  # Use user token for debug
            }
            
            response = requests.get(debug_url, params=params)
            response.raise_for_status()
            debug_data = response.json()
            
            token_data = debug_data.get('data', {})
            
            token_result = {
                "page_name": page_name,
                "page_id": page_id,
                "token_info": {
                    "is_valid": token_data.get('is_valid', False),
                    "expires_at": token_data.get('expires_at'),
                    "issued_at": token_data.get('issued_at'),
                    "scopes": token_data.get('scopes', []),
                    "type": token_data.get('type', 'unknown')
                },
                "success": True
            }
            
            # Convert timestamps to readable format
            expires_at = token_data.get('expires_at')
            if expires_at and expires_at > 0:
                expires_date = datetime.fromtimestamp(expires_at)
                print(f"✅ 成功: トークン有効期限 {expires_date.strftime('%Y年%m月%d日 %H:%M:%S')}")
            else:
                print(f"✅ 成功: 無期限トークン（期限なし）")
            
            print(f"   📊 データ: タイプ={token_data.get('type', 'unknown')}, 有効={token_data.get('is_valid', False)}")
            
        except Exception as e:
            token_result = {
                "page_name": page_name,
                "page_id": page_id,
                "success": False,
                "error": str(e)
            }
            print(f"❌ エラー: トークン情報の取得に失敗")
            print(f"   🔍 詳細: {e}")
        
        results["token_checks"].append(token_result)
        print()
    
    # Save results
    output_file = os.path.join(os.path.dirname(__file__), '02-output-data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 結果保存: {output_file}")
    
    # Summary
    total_checks = len(results["token_checks"])
    successful_checks = sum(1 for check in results["token_checks"] if check.get("success"))
    
    print(f"\n🏁 検証完了 - 実行結果サマリー")
    print(f"📊 総チェック数: {total_checks}")
    print(f"✅ 成功: {successful_checks}")
    print(f"❌ 失敗: {total_checks - successful_checks}")
    
    if successful_checks > 0:
        print("🎉 Page Access Tokenの有効期限を確認できました")
        print("🔍 次のステップ: Instagram Business Accountのデータ取得テストが可能です")
        return True
    else:
        print("⚠️ トークンの確認に失敗しました")
        return False

if __name__ == "__main__":
    success = check_token_expiration()
    sys.exit(0 if success else 1)