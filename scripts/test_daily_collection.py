#!/usr/bin/env python3
"""
Local test script for daily data collection
GitHub Actions実行前のローカルテスト用
"""

import asyncio
import os
import sys
from datetime import datetime

# Import the main collection script
from daily_data_collection import collect_all_instagram_data
from setup_environment import setup_environment, validate_database_connection
from report_generator import generate_collection_report, save_report_to_file

async def test_local_collection():
    """Test data collection locally before GitHub Actions deployment"""
    
    print("🧪 Daily Data Collection - ローカルテスト開始")
    print(f"📅 実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print(f"💻 実行環境: ローカル開発環境")
    print()
    
    # Step 1: Environment validation
    print("🔧 Step 1: 環境変数検証...")
    env_success = setup_environment()
    
    if not env_success:
        print("❌ 環境変数設定に問題があります。テストを中止します。")
        return False
    
    print()
    
    # Step 2: Database connectivity test
    print("🗄️ Step 2: データベース接続テスト...")
    db_success = validate_database_connection()
    
    if not db_success:
        print("❌ データベース接続に問題があります。テストを中止します。")
        return False
    
    print()
    
    # Step 3: Data collection test
    print("📊 Step 3: データ収集テスト実行...")
    
    try:
        # Set debug mode for local testing
        os.environ['DEBUG_MODE'] = 'true'
        
        # Run the actual data collection
        results = await collect_all_instagram_data()
        
        print()
        print("📋 Step 4: テスト結果分析...")
        
        # Analyze results
        success = results.get('success', False)
        accounts_processed = results.get('accounts_processed', 0)
        media_collected = results.get('media_posts_collected', 0)
        insights_collected = results.get('insights_collected', 0)
        account_insights = results.get('account_insights_collected', 0)
        errors = results.get('errors', [])
        
        print(f"   🔍 処理アカウント: {accounts_processed}件")
        print(f"   📸 投稿データ: {media_collected}件")
        print(f"   📊 投稿インサイト: {insights_collected}件")
        print(f"   📈 アカウントインサイト: {account_insights}件")
        print(f"   ❌ エラー数: {len(errors)}件")
        
        # Generate test report
        print(f"\n📄 Step 5: テストレポート生成...")
        report_path = save_report_to_file(results, "local_test_report.md")
        
        if report_path:
            print(f"   ✅ レポート保存: {os.path.basename(report_path)}")
        
        # Final assessment
        print(f"\n🏁 ローカルテスト完了")
        
        if success and accounts_processed > 0:
            print("✅ テスト成功: GitHub Actions でのデプロイ準備完了")
            print("🚀 次のステップ:")
            print("   1. GitHub リポジトリにコードをプッシュ")
            print("   2. GitHub Secrets の設定確認")
            print("   3. GitHub Actions ワークフローの手動実行テスト")
            return True
        else:
            print("⚠️ テスト部分成功: 問題を確認してください")
            if len(errors) > 0:
                print("エラー詳細:")
                for i, error in enumerate(errors, 1):
                    print(f"   {i}. {error}")
            return False
            
    except Exception as e:
        print(f"💥 テスト中に例外が発生: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_components():
    """Test individual components separately"""
    
    print("🔧 コンポーネント別テスト開始")
    
    # Test environment setup
    print("\n1. 環境設定テスト...")
    env_result = setup_environment()
    print(f"   結果: {'✅ 成功' if env_result else '❌ 失敗'}")
    
    # Test database connection
    print("\n2. データベース接続テスト...")
    db_result = validate_database_connection()
    print(f"   結果: {'✅ 成功' if db_result else '❌ 失敗'}")
    
    # Test report generation
    print("\n3. レポート生成テスト...")
    try:
        sample_results = {
            "execution_time": datetime.now().isoformat(),
            "success": True,
            "accounts_processed": 2,
            "media_posts_collected": 10,
            "insights_collected": 10,
            "account_insights_collected": 2,
            "errors": []
        }
        
        report = generate_collection_report(sample_results)
        print(f"   結果: ✅ 成功 ({len(report)}文字のレポート生成)")
        
        report_result = True
    except Exception as e:
        print(f"   結果: ❌ 失敗 - {str(e)}")
        report_result = False
    
    # Overall component test result
    all_passed = env_result and db_result and report_result
    print(f"\n🏁 コンポーネントテスト完了: {'✅ 全て成功' if all_passed else '❌ 一部失敗'}")
    
    return all_passed

if __name__ == "__main__":
    print("Instagram Daily Data Collection - ローカルテストスイート")
    print("=" * 60)
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--components":
        # Test individual components
        success = test_individual_components()
    else:
        # Run full integration test
        success = asyncio.run(test_local_collection())
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)