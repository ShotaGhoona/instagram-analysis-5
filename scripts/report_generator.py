#!/usr/bin/env python3
"""
Data Collection Report Generator
GitHub Actions実行結果のレポート生成
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

def generate_collection_report(results: Dict[str, Any]) -> str:
    """Generate human-readable collection report"""
    
    execution_time = results.get('execution_time', 'Unknown')
    success = results.get('success', False)
    
    # Parse execution time for display
    try:
        exec_dt = datetime.fromisoformat(execution_time.replace('Z', '+00:00'))
        formatted_time = exec_dt.strftime('%Y年%m月%d日 %H:%M:%S JST')
    except:
        formatted_time = execution_time
    
    report = f"""# Instagram Data Collection Report

## 📊 実行サマリー
- **実行日時**: {formatted_time}
- **総合結果**: {'✅ 成功' if success else '❌ 失敗'}
- **処理アカウント**: {results.get('accounts_processed', 0)}件
- **投稿データ**: {results.get('media_posts_collected', 0)}件収集
- **インサイト**: {results.get('insights_collected', 0)}件収集
- **アカウントインサイト**: {results.get('account_insights_collected', 0)}件収集

## 📋 詳細結果

### アカウント一覧
"""
    
    # Account details
    detailed_results = results.get('detailed_results', {})
    accounts = detailed_results.get('accounts', [])
    
    if accounts:
        for account in accounts:
            name = account.get('name', 'Unknown')
            username = account.get('username', 'unknown')
            has_token = '✅' if account.get('has_token', False) else '❌'
            report += f"- **{name}** (@{username}) - Token: {has_token}\n"
    else:
        report += "アカウント情報なし\n"
    
    # Media collection results
    report += f"\n### 📸 投稿データ収集結果\n"
    media_collection = detailed_results.get('media_collection', [])
    
    if media_collection:
        for media in media_collection:
            account_name = media.get('account', 'Unknown')
            result = media.get('result', {})
            success_status = '✅' if result.get('success', False) else '❌'
            collected = result.get('collected_posts', 0)
            saved = result.get('saved_posts', 0)
            
            report += f"- **{account_name}**: {success_status} {collected}件収集, {saved}件保存\n"
            
            if not result.get('success'):
                error = result.get('error', 'Unknown error')
                report += f"  - エラー: {error}\n"
    else:
        report += "投稿データ収集結果なし\n"
    
    # Insights collection results
    report += f"\n### 📊 投稿インサイト収集結果\n"
    insights_collection = detailed_results.get('insights_collection', [])
    
    if insights_collection:
        for insights in insights_collection:
            account_name = insights.get('account', 'Unknown')
            result = insights.get('result', {})
            success_status = '✅' if result.get('success', False) else '❌'
            successful = result.get('successful_media', 0)
            processed = result.get('processed_media', 0)
            
            report += f"- **{account_name}**: {success_status} {successful}/{processed} 投稿インサイト成功\n"
            
            if not result.get('success'):
                error = result.get('error', 'Unknown error')
                report += f"  - エラー: {error}\n"
    else:
        report += "投稿インサイト収集結果なし\n"
    
    # Account insights results
    report += f"\n### 📈 アカウントインサイト収集結果\n"
    account_insights = detailed_results.get('account_insights', {})
    
    if account_insights:
        insights_results = account_insights.get('insights_results', [])
        for account_result in insights_results:
            account_name = account_result.get('account_name', 'Unknown')
            result = account_result.get('result', {})
            success_status = '✅' if result.get('success', False) else '❌'
            metrics = result.get('collected_metrics', 0)
            saved = result.get('saved_records', 0)
            
            report += f"- **{account_name}**: {success_status} {metrics}メトリクス, {saved}件保存\n"
            
            if not result.get('success'):
                error = result.get('error', 'Unknown error')
                report += f"  - エラー: {error}\n"
    else:
        report += "アカウントインサイト収集結果なし\n"
    
    # Error summary
    report += f"\n## ❌ エラー詳細\n"
    errors = results.get('errors', [])
    
    if errors:
        for i, error in enumerate(errors, 1):
            report += f"{i}. {error}\n"
    else:
        report += "エラーなし ✅\n"
    
    # Next steps
    report += f"\n## 🎯 次のアクション\n"
    
    if success:
        report += """- データ収集は正常に完了しました
- 収集されたデータはSupabaseに保存されています
- 次回の自動実行: 明日の同時刻
"""
    else:
        report += """- データ収集でエラーが発生しました
- 上記のエラー詳細を確認してください
- Instagram APIトークンの有効期限をチェック
- Supabase接続状況を確認
- 必要に応じて手動でデータ収集を実行
"""
    
    report += f"\n---\n*このレポートは自動生成されました ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})*"
    
    return report

def save_report_to_file(results: Dict[str, Any], filename: str = None) -> str:
    """Save report to markdown file"""
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"collection_report_{timestamp}.md"
    
    filepath = os.path.join(os.path.dirname(__file__), filename)
    report_content = generate_collection_report(results)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"📄 レポート保存完了: {filename}")
        return filepath
    except Exception as e:
        print(f"❌ レポート保存失敗: {str(e)}")
        return ""

def load_results_from_file(filepath: str) -> Dict[str, Any]:
    """Load results from JSON file"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 結果ファイル読み込み失敗: {str(e)}")
        return {}

if __name__ == "__main__":
    # Example usage / Test mode
    import sys
    
    if len(sys.argv) > 1:
        # Load results from file and generate report
        results_file = sys.argv[1]
        results = load_results_from_file(results_file)
        
        if results:
            save_report_to_file(results)
        else:
            print("結果ファイルの読み込みに失敗しました")
            sys.exit(1)
    else:
        # Generate sample report for testing
        sample_results = {
            "execution_time": datetime.now().isoformat(),
            "success": True,
            "accounts_processed": 5,
            "media_posts_collected": 25,
            "insights_collected": 25,
            "account_insights_collected": 5,
            "detailed_results": {
                "accounts": [
                    {"name": "Test Account 1", "username": "test1", "has_token": True},
                    {"name": "Test Account 2", "username": "test2", "has_token": True}
                ],
                "media_collection": [
                    {"account": "Test Account 1", "result": {"success": True, "collected_posts": 12, "saved_posts": 12}},
                    {"account": "Test Account 2", "result": {"success": True, "collected_posts": 13, "saved_posts": 13}}
                ],
                "insights_collection": [
                    {"account": "Test Account 1", "result": {"success": True, "successful_media": 12, "processed_media": 12}},
                    {"account": "Test Account 2", "result": {"success": True, "successful_media": 13, "processed_media": 13}}
                ],
                "account_insights": {
                    "insights_results": [
                        {"account_name": "Test Account 1", "result": {"success": True, "collected_metrics": 2, "saved_records": 1}},
                        {"account_name": "Test Account 2", "result": {"success": True, "collected_metrics": 2, "saved_records": 1}}
                    ]
                }
            },
            "errors": []
        }
        
        print("🧪 サンプルレポート生成中...")
        report = generate_collection_report(sample_results)
        print(report)
        
        save_report_to_file(sample_results, "sample_report.md")