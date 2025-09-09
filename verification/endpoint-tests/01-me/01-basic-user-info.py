#!/usr/bin/env python3
"""
01-me endpoint verification script

Test the /me endpoint to retrieve current user information
This is the first step in Instagram Graph API verification.
"""

import sys
import os
import json
import requests
from datetime import datetime

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.api_client import InstagramAPIClient

def test_me_endpoint():
    """Test the /me endpoint to get current user information"""
    client = InstagramAPIClient()
    
    print("🚀 Instagram Graph API - /me エンドポイント検証を開始します")
    print(f"📅 検証実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print()
    
    # Test results structure
    results = {
        "endpoint": "/me",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "現在のユーザー情報取得とInstagram Business Account特定",
        "tests": []
    }
    
    # Test 1: Basic user info with Facebook Login
    print("🔍 テスト1: 基本ユーザー情報取得 (/me)")
    try:
        response = client.graph_api_request('/me', params={
            'fields': 'id,name,email'
        })
        
        test_result = {
            "test_name": "basic_user_info",
            "success": True,
            "data": response,
            "notes": "基本ユーザー情報の取得に成功"
        }
        
        print(f"✅ 成功: ユーザー情報を取得しました")
        print(f"   👤 ユーザーID: {response.get('id', 'N/A')}")
        print(f"   📛 名前: {response.get('name', 'N/A')}")
        print(f"   📧 メールアドレス: {response.get('email', 'N/A')}")
        
    except Exception as e:
        test_result = {
            "test_name": "basic_user_info",
            "success": False,
            "error": str(e),
            "notes": "基本ユーザー情報の取得に失敗"
        }
        print(f"❌ エラー: ユーザー情報の取得に失敗しました")
        print(f"   🔍 詳細: {e}")
    
    results["tests"].append(test_result)
    print()
    
    # Test 2: User accounts (pages) list
    print("🔍 テスト2: 管理ページ・アカウント一覧取得 (/me/accounts)")
    try:
        response = client.graph_api_request('/me/accounts', params={
            'fields': 'id,name,access_token,instagram_business_account'
        })
        
        test_result = {
            "test_name": "user_accounts",
            "success": True,
            "data": response,
            "notes": "管理ページ・アカウント一覧の取得に成功"
        }
        
        account_count = len(response.get('data', []))
        print(f"✅ 成功: {account_count}件のアカウントを取得しました")
        
        # Look for Instagram Business Accounts
        instagram_accounts = []
        for account in response.get('data', []):
            if 'instagram_business_account' in account:
                instagram_accounts.append({
                    'page_id': account['id'],
                    'page_name': account['name'],
                    'ig_account': account['instagram_business_account']
                })
        
        if instagram_accounts:
            print(f"📊 データ: {len(instagram_accounts)}件のInstagram Businessアカウントを発見:")
            for ig_acc in instagram_accounts:
                print(f"     📄 ページ名: {ig_acc['page_name']}")
                print(f"     🆔 ページID: {ig_acc['page_id']}")
                print(f"     📸 Instagram Business Account ID: {ig_acc['ig_account']['id']}")
        else:
            print("⚠️ 警告: Instagram Business Accountが見つかりませんでした")
            print("   🔧 対策: Facebook Business ManagerでInstagramアカウントとの連携を確認してください")
        
        test_result["instagram_accounts"] = instagram_accounts
        test_result["instagram_account_count"] = len(instagram_accounts)
        
    except Exception as e:
        test_result = {
            "test_name": "user_accounts",
            "success": False,
            "error": str(e),
            "notes": "管理ページ・アカウント一覧の取得に失敗"
        }
        print(f"❌ エラー: 管理ページ・アカウント一覧の取得に失敗しました")
        print(f"   🔍 詳細: {e}")
    
    results["tests"].append(test_result)
    print()
    
    # Save results to JSON file
    output_file = os.path.join(os.path.dirname(__file__), '01-output-data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"💾 結果保存: {output_file}")
    
    # Generate summary
    total_tests = len(results["tests"])
    successful_tests = sum(1 for test in results["tests"] if test["success"])
    failed_tests = total_tests - successful_tests
    
    print(f"\n🏁 検証完了 - 実行結果サマリー")
    print(f"📊 総テスト数: {total_tests}")
    print(f"✅ 成功: {successful_tests}")
    print(f"❌ 失敗: {failed_tests}")
    
    if successful_tests == total_tests:
        print("🎉 すべてのテストが成功しました！次のエンドポイント検証に進めます")
        return True
    else:
        print("⚠️ 一部のテストが失敗しました。エラー内容を確認して設定を見直してください")
        return False

if __name__ == "__main__":
    success = test_me_endpoint()
    sys.exit(0 if success else 1)