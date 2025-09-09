#!/usr/bin/env python3
"""
Instagram Daily Data Collection Script

GitHub Actions用の統合データ収集スクリプト
- 全アカウントの基本情報更新
- 投稿データ収集（新規検出・保存）
- インサイトデータ収集（投稿毎）
- アカウントインサイト収集（アカウント毎）
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, Any, List
import json

# Backend path setup
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from repositories.instagram_repository import instagram_repository
from services.instagram_service import instagram_service

async def collect_all_instagram_data() -> Dict[str, Any]:
    """Complete Instagram data collection pipeline"""
    
    print("🚀 Instagram Daily Data Collection 開始")
    print(f"📅 実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print(f"🌍 タイムゾーン: JST (GitHub Actions: UTC)")
    print()
    
    results = {
        "execution_time": datetime.now().isoformat(),
        "success": True,
        "accounts_processed": 0,
        "media_posts_collected": 0,
        "insights_collected": 0,
        "account_insights_collected": 0,
        "detailed_results": {
            "accounts": [],
            "media_collection": [],
            "insights_collection": [],
            "account_insights": []
        },
        "errors": []
    }
    
    try:
        # 1. Get all Instagram accounts from database
        print("📋 Step 0: データベースからアカウント一覧取得...")
        accounts = await instagram_repository.get_all()
        
        if not accounts:
            error_msg = "No Instagram accounts found in database"
            results["errors"].append(error_msg)
            results["success"] = False
            print(f"❌ {error_msg}")
            return results
        
        print(f"✅ 取得完了: {len(accounts)}件のアカウント")
        for account in accounts:
            print(f"   📱 {account.name} (@{account.username}) - {account.ig_user_id}")
        print()
        
        results["accounts_processed"] = len(accounts)
        
        # Convert to service format
        accounts_data = []
        for account in accounts:
            account_data = {
                'name': account.name,
                'ig_user_id': account.ig_user_id,
                'access_token': account.access_token,
                'username': account.username
            }
            accounts_data.append(account_data)
            results["detailed_results"]["accounts"].append({
                "name": account.name,
                "username": account.username,
                "ig_user_id": account.ig_user_id,
                "has_token": bool(account.access_token)
            })
        
        # 2. Collect media posts for all accounts
        print("📸 Step 1: 投稿データ収集...")
        media_results = []
        total_media_collected = 0
        
        for account_data in accounts_data:
            print(f"   🔍 {account_data['name']} の投稿データ収集中...")
            
            try:
                result = await instagram_service.collect_media_posts(
                    account_data['ig_user_id'], 
                    account_data['access_token']
                )
                
                account_result = {
                    "account": account_data['name'],
                    "ig_user_id": account_data['ig_user_id'],
                    "result": result
                }
                media_results.append(account_result)
                results["detailed_results"]["media_collection"].append(account_result)
                
                if result.get("success"):
                    collected = result.get("collected_posts", 0)
                    total_media_collected += collected
                    print(f"   ✅ {account_data['name']}: {collected}件の投稿を収集")
                else:
                    error_msg = f"Media posts failed for {account_data['name']}: {result.get('error', 'Unknown error')}"
                    results["errors"].append(error_msg)
                    print(f"   ❌ {account_data['name']}: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                error_msg = f"Exception in media collection for {account_data['name']}: {str(e)}"
                results["errors"].append(error_msg)
                print(f"   ❌ {account_data['name']}: 例外発生 - {str(e)}")
        
        results["media_posts_collected"] = total_media_collected
        print(f"📸 投稿データ収集完了: 合計 {total_media_collected}件")
        print()
        
        # 3. Collect media insights for all accounts
        print("📊 Step 2: 投稿インサイト収集...")
        insights_results = []
        total_insights_collected = 0
        
        for account_data in accounts_data:
            print(f"   🔍 {account_data['name']} のインサイトデータ収集中...")
            
            try:
                result = await instagram_service.collect_all_media_insights(
                    account_data['ig_user_id'], 
                    account_data['access_token']
                )
                
                account_result = {
                    "account": account_data['name'],
                    "ig_user_id": account_data['ig_user_id'],
                    "result": result
                }
                insights_results.append(account_result)
                results["detailed_results"]["insights_collection"].append(account_result)
                
                if result.get("success"):
                    successful = result.get("successful_media", 0)
                    processed = result.get("processed_media", 0)
                    total_insights_collected += successful
                    print(f"   ✅ {account_data['name']}: {successful}/{processed} 投稿のインサイト収集成功")
                else:
                    error_msg = f"Media insights failed for {account_data['name']}: {result.get('error', 'Unknown error')}"
                    results["errors"].append(error_msg)
                    print(f"   ❌ {account_data['name']}: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                error_msg = f"Exception in insights collection for {account_data['name']}: {str(e)}"
                results["errors"].append(error_msg)
                print(f"   ❌ {account_data['name']}: 例外発生 - {str(e)}")
        
        results["insights_collected"] = total_insights_collected
        print(f"📊 投稿インサイト収集完了: 合計 {total_insights_collected}件")
        print()
        
        # 4. Collect account insights
        print("📈 Step 3: アカウントインサイト収集...")
        
        try:
            account_insights_result = await instagram_service.collect_all_account_insights(accounts_data)
            results["detailed_results"]["account_insights"] = account_insights_result
            
            if account_insights_result.get("success"):
                successful_accounts = account_insights_result.get("successful_accounts", 0)
                results["account_insights_collected"] = successful_accounts
                print(f"✅ アカウントインサイト収集完了: {successful_accounts}/{len(accounts_data)} アカウント成功")
                
                # Display results for each account
                for result in account_insights_result.get("insights_results", []):
                    account_name = result.get("account_name")
                    account_result = result.get("result", {})
                    
                    if account_result.get("success"):
                        metrics = account_result.get("collected_metrics", 0)
                        saved = account_result.get("saved_records", 0)
                        print(f"   ✅ {account_name}: {metrics} メトリクス, {saved}件保存")
                    else:
                        print(f"   ❌ {account_name}: {account_result.get('error', 'Unknown error')}")
            else:
                error_msg = f"Account insights failed: {account_insights_result.get('error', 'Unknown error')}"
                results["errors"].append(error_msg)
                print(f"❌ {error_msg}")
                
        except Exception as e:
            error_msg = f"Exception in account insights collection: {str(e)}"
            results["errors"].append(error_msg)
            print(f"❌ {error_msg}")
        
        print()
        
        # 5. Final Summary
        print(f"🏁 Instagram Daily Data Collection 完了")
        print(f"📊 収集サマリー:")
        print(f"   🔍 処理アカウント: {results['accounts_processed']}件")
        print(f"   📸 投稿データ: {results['media_posts_collected']}件")
        print(f"   📊 投稿インサイト: {results['insights_collected']}件")
        print(f"   📈 アカウントインサイト: {results['account_insights_collected']}件")
        print(f"   ❌ エラー: {len(results['errors'])}件")
        
        # Determine overall success
        if len(results["errors"]) > 0:
            results["success"] = False
            print(f"\n⚠️ 一部エラーが発生しました:")
            for i, error in enumerate(results["errors"], 1):
                print(f"   {i}. {error}")
        else:
            print(f"\n🎉 全ての処理が正常に完了しました！")
        
        return results
        
    except Exception as e:
        error_msg = f"Critical error in data collection: {str(e)}"
        results["errors"].append(error_msg)
        results["success"] = False
        print(f"💥 {error_msg}")
        import traceback
        traceback.print_exc()
        return results

def save_results_to_file(results: Dict[str, Any]):
    """Save results to a JSON file for debugging"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"collection_results_{timestamp}.json"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📄 詳細結果を保存: {filename}")
        
    except Exception as e:
        print(f"⚠️ 結果ファイル保存に失敗: {str(e)}")

if __name__ == "__main__":
    # Set environment variables for debugging
    debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    
    if debug_mode:
        print("🐛 DEBUG MODE: 詳細ログを有効化")
    
    # Run collection
    results = asyncio.run(collect_all_instagram_data())
    
    # Save detailed results if in debug mode or if errors occurred
    if debug_mode or len(results.get("errors", [])) > 0:
        save_results_to_file(results)
    
    # Print final status
    success = results.get("success", False)
    
    if success:
        print("\n✅ Data collection completed successfully")
        sys.exit(0)
    else:
        print(f"\n❌ Data collection completed with {len(results.get('errors', []))} errors")
        sys.exit(1)