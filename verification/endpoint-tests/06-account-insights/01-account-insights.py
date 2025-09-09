#!/usr/bin/env python3
"""
Account Insights Verification Script

Test GET /{ig-user-id}/insights?metric=impressions,profile_views,website_clicks&period=day
for daily account-level insights data collection.
"""

import sys
import os
import json
import requests
from datetime import datetime, timedelta

# Add parent directory to path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Simplified API client to avoid dependency issues
import requests

class SimpleAPIClient:
    def __init__(self):
        self.graph_api_url = "https://graph.facebook.com/v18.0"
    
    def graph_api_request(self, endpoint, params=None):
        """Make a Graph API request"""
        try:
            # Remove leading slash from endpoint to avoid double slashes
            endpoint = endpoint.lstrip('/')
            url = f"{self.graph_api_url}/{endpoint}"
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Request Exception: {e}")
            return None

def test_account_insights():
    """Test account-level insights retrieval for daily insights collection"""
    
    print("🚀 Account Insights 検証を開始します")
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
    print("   📝 注: 全アカウントのアカウントレベルインサイトを取得します")
    print()
    
    # Results structure
    results = {
        "endpoint": "/{ig-user-id}/insights (Account Insights)",
        "timestamp": datetime.now().isoformat(),
        "検証概要": "毎日収集用アカウントレベルインサイトテスト",
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
    
    client = SimpleAPIClient()
    
    # Test metrics to verify (based on API error response)
    insight_metrics = ['profile_views', 'website_clicks']
    # Additional available metrics for future consideration: 
    # 'reach', 'follower_count', 'total_interactions', 'accounts_engaged'
    
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
        
        # Test 1: Combined metrics request
        print(f"   🧪 テスト1: 複数メトリクス一括取得...")
        try:
            combined_params = {
                'metric': ','.join(insight_metrics),
                'period': 'day',
                'metric_type': 'total_value',
                'access_token': page_token
            }
            
            response = client.graph_api_request(f'/{ig_account_id}/insights', params=combined_params)
            
            if response and 'data' in response:
                insights_data = response['data']
                test_result = {
                    "test_name": "combined_account_insights",
                    "success": True,
                    "data": response,
                    "notes": "アカウントレベルインサイト一括取得成功"
                }
                
                print(f"   ✅ 成功: {len(insights_data)}件のメトリクスを取得しました")
                
                # Display each metric
                for insight in insights_data:
                    metric_name = insight.get('name', 'Unknown')
                    metric_period = insight.get('period', 'Unknown')
                    values = insight.get('values', [])
                    
                    if values and len(values) > 0:
                        latest_value = values[0].get('value', 0)
                        end_time = values[0].get('end_time', 'N/A')
                        print(f"      📊 {metric_name}: {latest_value:,} ({metric_period}) - {end_time}")
                    else:
                        print(f"      ❌ {metric_name}: データなし")
                
            else:
                test_result = {
                    "test_name": "combined_account_insights",
                    "success": False,
                    "error": "API response is None or missing data",
                    "notes": "アカウントレベルインサイト一括取得失敗"
                }
                print(f"   ❌ 失敗: アカウントインサイトの取得に失敗")
                
        except Exception as e:
            test_result = {
                "test_name": "combined_account_insights",
                "success": False,
                "error": str(e),
                "notes": "アカウントレベルインサイト一括取得で例外発生"
            }
            print(f"   ❌ 例外: {e}")
        
        account_result["tests"].append(test_result)
        
        # Test 2: Individual metrics validation (if combined request succeeded)
        if test_result.get("success"):
            print(f"   🧪 テスト2: 個別メトリクス検証...")
            try:
                individual_results = {}
                
                for metric in insight_metrics:
                    individual_params = {
                        'metric': metric,
                        'period': 'day',
                        'metric_type': 'total_value',
                        'access_token': page_token
                    }
                    
                    metric_response = client.graph_api_request(f'/{ig_account_id}/insights', params=individual_params)
                    
                    if metric_response and 'data' in metric_response and len(metric_response['data']) > 0:
                        metric_data = metric_response['data'][0]
                        values = metric_data.get('values', [])
                        
                        if values and len(values) > 0:
                            metric_value = values[0].get('value', 0)
                            individual_results[metric] = {
                                "available": True,
                                "value": metric_value,
                                "raw_data": metric_data
                            }
                            print(f"      ✅ {metric}: {metric_value:,}")
                        else:
                            individual_results[metric] = {
                                "available": False,
                                "value": None,
                                "error": "Empty values array"
                            }
                            print(f"      ❌ {metric}: データが空")
                    else:
                        individual_results[metric] = {
                            "available": False,
                            "value": None,
                            "error": "No response or empty data"
                        }
                        print(f"      ❌ {metric}: レスポンスなし")
                
                individual_test_result = {
                    "test_name": "individual_metrics",
                    "success": True,
                    "data": individual_results,
                    "notes": "個別メトリクス検証完了"
                }
                
            except Exception as e:
                individual_test_result = {
                    "test_name": "individual_metrics", 
                    "success": False,
                    "error": str(e),
                    "notes": "個別メトリクス検証で例外発生"
                }
                print(f"   ❌ 例外: {e}")
            
            account_result["tests"].append(individual_test_result)
        
        # Test 3: Time period validation (test different periods)
        print(f"   🧪 テスト3: 期間パラメータ検証...")
        try:
            periods_to_test = ['day']  # Focus on 'day' as that's what we need
            period_results = {}
            
            for period in periods_to_test:
                period_params = {
                    'metric': 'profile_views',  # Test with profile_views as sample
                    'period': period,
                    'metric_type': 'total_value',
                    'access_token': page_token
                }
                
                period_response = client.graph_api_request(f'/{ig_account_id}/insights', params=period_params)
                
                if period_response and 'data' in period_response and len(period_response['data']) > 0:
                    period_data = period_response['data'][0]
                    values = period_data.get('values', [])
                    
                    if values and len(values) > 0:
                        period_value = values[0].get('value', 0)
                        period_results[period] = {
                            "available": True,
                            "value": period_value,
                            "sample_metric": "profile_views"
                        }
                        print(f"      ✅ period={period}: profile_views={period_value:,}")
                    else:
                        period_results[period] = {
                            "available": False,
                            "error": "Empty values"
                        }
                        print(f"      ❌ period={period}: データが空")
                else:
                    period_results[period] = {
                        "available": False,
                        "error": "No response"
                    }
                    print(f"      ❌ period={period}: レスポンスなし")
            
            period_test_result = {
                "test_name": "period_validation",
                "success": True,
                "data": period_results,
                "notes": "期間パラメータ検証完了"
            }
            
        except Exception as e:
            period_test_result = {
                "test_name": "period_validation",
                "success": False,
                "error": str(e),
                "notes": "期間パラメータ検証で例外発生"
            }
            print(f"   ❌ 例外: {e}")
        
        account_result["tests"].append(period_test_result)
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
    metric_success_count = {metric: 0 for metric in insight_metrics}
    
    for account in results["account_tests"]:
        account_success = False
        for test in account.get("tests", []):
            if test.get("test_name") == "combined_account_insights" and test.get("success"):
                account_success = True
                break
        
        if account_success:
            successful_accounts += 1
        
        # Count individual metric success
        for test in account.get("tests", []):
            if test.get("test_name") == "individual_metrics" and test.get("success"):
                individual_data = test.get("data", {})
                for metric in insight_metrics:
                    if individual_data.get(metric, {}).get("available"):
                        metric_success_count[metric] += 1
    
    print(f"\n🏁 検証完了 - 実行結果サマリー")
    print(f"📊 総アカウント数: {total_accounts}")
    print(f"✅ 成功したアカウント: {successful_accounts}")
    print(f"❌ 失敗したアカウント: {total_accounts - successful_accounts}")
    
    print(f"\n📈 メトリクス別成功率:")
    for metric, success_count in metric_success_count.items():
        print(f"   {metric}: {success_count}/{total_accounts} 件成功")
    
    if successful_accounts > 0:
        print("\n🎉 アカウントレベルインサイトの取得に成功しました！")
        print("🔍 次のステップ: 毎日のデータ収集でこれらのインサイトを定期取得できます")
        return True
    else:
        print("\n⚠️ アカウントレベルインサイトの取得に失敗しました")
        print("🔧 対策: Page Access Tokenとinsights権限の設定を確認してください")
        return False

if __name__ == "__main__":
    success = test_account_insights()
    sys.exit(0 if success else 1)