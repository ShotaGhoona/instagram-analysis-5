#!/usr/bin/env python3
"""
Environment Setup for GitHub Actions
GitHub Actions実行前の環境変数チェック
"""

import os
import sys

def setup_environment():
    """Setup environment variables for data collection"""
    
    print("🔧 Environment Setup - 環境変数チェック開始")
    print(f"📅 実行日時: {os.environ.get('GITHUB_RUN_ID', 'ローカル実行')}")
    print()
    
    # Required environment variables
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'INSTAGRAM_APP_ID',
        'INSTAGRAM_APP_SECRET'
    ]
    
    # Optional environment variables (for debugging/monitoring)
    optional_vars = [
        'DEBUG_MODE',
        'GITHUB_REPOSITORY',
        'GITHUB_RUN_ID',
        'GITHUB_SHA'
    ]
    
    print("📋 必須環境変数チェック:")
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values for security
            if 'SECRET' in var or 'KEY' in var:
                masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
                print(f"   ✅ {var}: {masked_value}")
            else:
                print(f"   ✅ {var}: {value}")
        else:
            missing_vars.append(var)
            print(f"   ❌ {var}: 未設定")
    
    print(f"\n📋 オプション環境変数:")
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {value}")
        else:
            print(f"   ⚪ {var}: 未設定 (オプション)")
    
    # Check if running in GitHub Actions
    if os.getenv('GITHUB_ACTIONS'):
        print(f"\n🤖 GitHub Actions環境で実行中")
        print(f"   📁 Repository: {os.getenv('GITHUB_REPOSITORY', 'Unknown')}")
        print(f"   🏃 Run ID: {os.getenv('GITHUB_RUN_ID', 'Unknown')}")
        print(f"   🔀 SHA: {os.getenv('GITHUB_SHA', 'Unknown')[:8]}...")
    else:
        print(f"\n💻 ローカル環境で実行中")
        print(f"   🏠 作業ディレクトリ: {os.getcwd()}")
        print(f"   🐍 Python: {sys.version}")
    
    # Final validation
    if missing_vars:
        print(f"\n❌ 環境変数チェック失敗")
        print(f"未設定の必須変数: {', '.join(missing_vars)}")
        print(f"\n🔧 対策:")
        print(f"1. GitHub リポジトリの Settings > Secrets and variables > Actions")
        print(f"2. 以下の変数を Repository secrets に追加:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    else:
        print(f"\n✅ 環境変数チェック成功")
        print(f"全ての必須環境変数が設定されています")
        return True

def validate_database_connection():
    """Validate Supabase database connection"""
    try:
        print(f"\n🗄️ データベース接続チェック...")
        
        # Check required environment variables for database connection
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            print(f"   ❌ データベース接続用環境変数が不足")
            return False
        
        # Add backend path for imports
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
        
        from utils.supabase_client import supabase_client
        
        # Test connection using the utility client
        client = supabase_client.client
        
        # Simple connectivity test
        result = client.table('instagram_accounts').select('count').execute()
        
        print(f"   ✅ Supabase接続成功")
        return True
        
    except Exception as e:
        print(f"   ❌ Supabase接続失敗: {str(e)}")
        return False

if __name__ == "__main__":
    success = setup_environment()
    
    # Also validate database connection if environment is set up correctly
    if success:
        db_success = validate_database_connection()
        success = success and db_success
    
    # Exit with appropriate code
    if success:
        print(f"\n🎉 環境セットアップ完了 - データ収集を開始できます")
        sys.exit(0)
    else:
        print(f"\n💥 環境セットアップ失敗 - 設定を確認してください")
        sys.exit(1)