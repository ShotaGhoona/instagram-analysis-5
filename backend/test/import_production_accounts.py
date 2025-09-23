#!/usr/bin/env python3
"""
Production Instagram Accounts Import Script
instagram_accounts_rows.csvからSupabaseのinstagram_accountsテーブルにデータ投入
"""

import csv
import sys
import os
from datetime import datetime
import asyncio

# Backend path setup
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from repositories.instagram_repository import instagram_repository
from models.instagram import InstagramAccount

def parse_csv_data(csv_file_path):
    """CSVファイルを読み込んでデータベース形式に変換"""
    print(f"📁 CSVファイル読み込み開始: {csv_file_path}")
    
    accounts_data = []
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row_num, row in enumerate(reader, start=2):  # ヘッダー行は1行目
                try:
                    # CSVフィールドからデータベーススキーマへのマッピング
                    account_data = {
                        'name': row['account_name'],
                        'ig_user_id': row['instagram_user_id'],
                        'access_token': row['access_token_encrypted'],  # 復号化は後で対応
                        'username': row['username'],
                        'profile_picture_url': row['profile_picture_url']
                    }
                    
                    # データバリデーション
                    if not account_data['ig_user_id'] or not account_data['username']:
                        print(f"⚠️  行 {row_num}: 必須フィールドが不足 - スキップ")
                        continue
                    
                    accounts_data.append(account_data)
                    print(f"✅ 行 {row_num}: {account_data['name']} (@{account_data['username']})")
                    
                except Exception as e:
                    print(f"❌ 行 {row_num}: データ変換エラー - {str(e)}")
                    continue
        
        print(f"\n📊 CSVデータ解析完了: {len(accounts_data)}件の有効なアカウントデータ")
        return accounts_data
        
    except Exception as e:
        print(f"💥 CSVファイル読み込みエラー: {str(e)}")
        return []

async def check_existing_accounts():
    """既存のアカウント一覧を取得"""
    print(f"\n🔍 既存アカウント確認中...")
    
    try:
        existing_accounts = await instagram_repository.get_all()
        print(f"📋 既存アカウント数: {len(existing_accounts)}件")
        
        for account in existing_accounts:
            print(f"   📱 {account.name} (@{account.username}) - {account.ig_user_id}")
        
        return {account.ig_user_id: account for account in existing_accounts}
        
    except Exception as e:
        print(f"❌ 既存アカウント取得エラー: {str(e)}")
        return {}

async def import_new_accounts(accounts_data, existing_accounts):
    """新規アカウントのみをデータベースに投入"""
    print(f"\n🚀 新規アカウント投入開始...")
    
    imported_count = 0
    skipped_count = 0
    error_count = 0
    
    for account_data in accounts_data:
        ig_user_id = account_data['ig_user_id']
        username = account_data['username']
        name = account_data['name']
        
        # 重複チェック
        if ig_user_id in existing_accounts:
            print(f"⏭️  {name} (@{username}): 既存アカウント - スキップ")
            skipped_count += 1
            continue
        
        try:
            # InstagramAccountオブジェクトを作成
            account = InstagramAccount(
                name=account_data['name'],
                ig_user_id=account_data['ig_user_id'],
                access_token=account_data['access_token'],
                username=account_data['username'],
                profile_picture_url=account_data['profile_picture_url']
            )
            
            # データベースに投入
            new_account = await instagram_repository.create(account)
            
            print(f"✅ {name} (@{username}): 投入成功 - ID: {new_account.id}")
            imported_count += 1
            
        except Exception as e:
            print(f"❌ {name} (@{username}): 投入失敗 - {str(e)}")
            error_count += 1
    
    print(f"\n📊 投入結果:")
    print(f"   ✅ 新規投入: {imported_count}件")
    print(f"   ⏭️  スキップ: {skipped_count}件")
    print(f"   ❌ エラー: {error_count}件")
    
    return imported_count, skipped_count, error_count

async def verify_final_state():
    """最終的なアカウント状態を確認"""
    print(f"\n🔍 最終確認: 全アカウント一覧")
    
    try:
        all_accounts = await instagram_repository.get_all()
        print(f"📋 合計アカウント数: {len(all_accounts)}件")
        
        for i, account in enumerate(all_accounts, 1):
            print(f"   {i:2d}. {account.name} (@{account.username}) - {account.ig_user_id}")
        
        return len(all_accounts)
        
    except Exception as e:
        print(f"❌ 最終確認エラー: {str(e)}")
        return 0

async def main():
    """メイン処理"""
    print("🎯 Instagram本番アカウントCSV投入開始")
    print(f"📅 実行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print()
    
    # CSVファイルパス
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'instagram_accounts_rows.csv')
    
    if not os.path.exists(csv_file_path):
        print(f"💥 エラー: CSVファイルが見つかりません - {csv_file_path}")
        return False
    
    try:
        # 1. CSVデータ解析
        accounts_data = parse_csv_data(csv_file_path)
        if not accounts_data:
            print("💥 CSVデータが空です")
            return False
        
        # 2. 既存アカウント確認
        existing_accounts = await check_existing_accounts()
        
        # 3. 新規アカウント投入
        imported_count, skipped_count, error_count = await import_new_accounts(accounts_data, existing_accounts)
        
        # 4. 最終確認
        total_accounts = await verify_final_state()
        
        # 5. 結果サマリー
        print(f"\n🏁 CSV投入完了")
        print(f"📊 結果サマリー:")
        print(f"   📥 CSV読み込み: {len(accounts_data)}件")
        print(f"   ✅ 新規投入: {imported_count}件")
        print(f"   ⏭️  既存スキップ: {skipped_count}件")
        print(f"   ❌ エラー: {error_count}件")
        print(f"   📋 合計アカウント: {total_accounts}件")
        
        if error_count == 0:
            print(f"\n🎉 全ての処理が正常に完了しました！")
            return True
        else:
            print(f"\n⚠️  一部エラーがありましたが、可能な分は投入完了")
            return True
            
    except Exception as e:
        print(f"💥 予期しないエラー: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    
    if success:
        print("\n✅ スクリプト実行完了")
        sys.exit(0)
    else:
        print("\n❌ スクリプト実行失敗")
        sys.exit(1)