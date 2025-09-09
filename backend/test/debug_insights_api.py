#!/usr/bin/env python3
"""
Instagram Insights API デバッグスクリプト
例外 - 0 エラーの詳細調査
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(__file__))

from external.instagram_client import InstagramAPIClient
from repositories.instagram_repository import instagram_repository
import requests

async def debug_insights_api():
    """Debug Instagram Insights API calls to identify the root cause"""
    
    print("🔍 Instagram Insights API デバッグ開始")
    print(f"📅 実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print()
    
    # Get test account (use 有限会社カネタケ - known to work in verification)
    try:
        accounts = await instagram_repository.get_all()
        kanetake_account = None
        
        for account in accounts:
            if "カネタケ" in account.name:
                kanetake_account = account
                break
        
        if not kanetake_account:
            print("❌ カネタケアカウントが見つかりません")
            return False
            
        print(f"🎯 テスト対象: {kanetake_account.name}")
        print(f"   📸 IG User ID: {kanetake_account.ig_user_id}")
        print(f"   🔑 Access Token: {kanetake_account.access_token[:20]}...")
        
    except Exception as e:
        print(f"❌ アカウント取得エラー: {str(e)}")
        return False
    
    # Get test media
    try:
        media_posts = await instagram_repository.get_media_posts(kanetake_account.ig_user_id, 1)
        if not media_posts:
            print("❌ 投稿データがありません")
            return False
        
        test_media = media_posts[0]
        media_id = test_media['ig_media_id']
        media_type = test_media.get('media_type', 'UNKNOWN')
        
        print(f"📸 テスト投稿: {media_id}")
        print(f"   📝 メディアタイプ: {media_type}")
        print()
        
    except Exception as e:
        print(f"❌ 投稿データ取得エラー: {str(e)}")
        return False
    
    # Debug 1: Direct API call without our wrapper
    print("🧪 デバッグ1: 直接API呼び出し")
    try:
        url = f"https://graph.facebook.com/v23.0/{media_id}/insights"
        params = {
            'metric': 'reach',
            'access_token': kanetake_account.access_token
        }
        
        print(f"   🌐 URL: {url}")
        print(f"   📋 Params: {params}")
        print(f"   🔄 リクエスト送信中...")
        
        response = requests.get(url, params=params)
        
        print(f"   📊 Status Code: {response.status_code}")
        print(f"   📄 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                print(f"   ✅ JSON Response: {json.dumps(response_data, indent=2)}")
            except json.JSONDecodeError:
                print(f"   ❌ JSON Decode Error")
                print(f"   📝 Raw Response: {response.text}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   📝 Error Response: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   📝 Raw Error: {response.text}")
                
    except Exception as e:
        print(f"   ❌ 直接API例外: {str(e)}")
    
    print()
    
    # Debug 2: Our API client with detailed logging
    print("🧪 デバッグ2: APIクライアント詳細ログ")
    try:
        client = InstagramAPIClient()
        
        # Test graph_api_request method directly
        print("   🔄 graph_api_request メソッドテスト...")
        
        endpoint = f"/{media_id}/insights"
        params = {
            'metric': 'reach',
            'access_token': kanetake_account.access_token
        }
        
        print(f"   📍 Endpoint: {endpoint}")
        print(f"   📋 Parameters: {params}")
        
        # Direct call to graph_api_request
        result = client.graph_api_request(endpoint, params)
        
        print(f"   📊 Result Type: {type(result)}")
        print(f"   📄 Result Content: {json.dumps(result, indent=2, default=str)}")
        
        if result and "success" in result:
            if result["success"]:
                print(f"   ✅ graph_api_request 成功")
                if "data" in result:
                    print(f"   📝 Data: {result['data']}")
            else:
                print(f"   ❌ graph_api_request 失敗")
                print(f"   📝 Error: {result.get('error', 'Unknown')}")
                print(f"   📝 Status Code: {result.get('status_code', 'Unknown')}")
                print(f"   📝 Error Data: {result.get('error_data', 'Unknown')}")
        
    except Exception as e:
        print(f"   ❌ APIクライアント例外: {str(e)}")
        import traceback
        print(f"   📝 Traceback: {traceback.format_exc()}")
    
    print()
    
    # Debug 3: Token validation
    print("🧪 デバッグ3: アクセストークン検証")
    try:
        # Test with /me endpoint (basic token validation)
        me_url = f"https://graph.facebook.com/v23.0/me"
        me_params = {'access_token': kanetake_account.access_token}
        
        me_response = requests.get(me_url, params=me_params)
        print(f"   📊 /me Status: {me_response.status_code}")
        
        if me_response.status_code == 200:
            me_data = me_response.json()
            print(f"   ✅ Token Valid - User: {me_data.get('name', 'Unknown')}")
        else:
            print(f"   ❌ Token Invalid")
            try:
                error_data = me_response.json()
                print(f"   📝 Token Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   📝 Token Raw Error: {me_response.text}")
                
    except Exception as e:
        print(f"   ❌ トークン検証例外: {str(e)}")
    
    print()
    print("🏁 デバッグ完了")
    return True

if __name__ == "__main__":
    success = asyncio.run(debug_insights_api())
    sys.exit(0 if success else 1)