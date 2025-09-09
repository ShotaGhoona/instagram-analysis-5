#!/usr/bin/env python3
"""
データベーステーブル作成確認スクリプト
B0102: テーブル作成の確認用
"""

from core.database import database

def test_table_existence():
    """テーブル作成確認"""
    print("🔍 テーブル作成確認開始...")
    
    tables = [
        'users',
        'instagram_accounts', 
        'daily_account_stats',
        'media_posts',
        'daily_media_stats'
    ]
    
    try:
        client = database.client
        
        for table in tables:
            # テーブルの存在確認（レコード数取得）
            result = client.table(table).select("count", count="exact").execute()
            print(f"✅ {table}: {result.count}件")
            
        print("\n🎉 全テーブル作成確認完了")
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_sample_data():
    """サンプルデータ確認"""
    print("\n🔍 サンプルデータ確認開始...")
    
    try:
        client = database.client
        
        # 各テーブルからサンプルデータ1件取得
        tables_data = {
            'users': 'username',
            'instagram_accounts': 'name', 
            'daily_account_stats': 'date',
            'media_posts': 'ig_media_id',
            'daily_media_stats': 'date'
        }
        
        for table, field in tables_data.items():
            result = client.table(table).select(f"{field}").limit(1).execute()
            if result.data:
                print(f"✅ {table}: {result.data[0][field]}")
            else:
                print(f"⚠️ {table}: データなし")
                
        print("\n🎉 サンプルデータ確認完了")
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_crud_operations():
    """基本CRUD操作テスト"""
    print("\n🔍 CRUD操作テスト開始...")
    
    try:
        client = database.client
        
        # テスト用ユーザー作成
        test_user_data = {
            'username': 'crud_test_user',
            'password_hash': 'test_hash_123'
        }
        
        # CREATE
        result = client.table('users').insert(test_user_data).execute()
        user_id = result.data[0]['id']
        print(f"✅ CREATE: ユーザーID {user_id} 作成")
        
        # READ
        result = client.table('users').select("*").eq('id', user_id).execute()
        print(f"✅ READ: {result.data[0]['username']}")
        
        # UPDATE
        client.table('users').update({'username': 'crud_updated_user'}).eq('id', user_id).execute()
        result = client.table('users').select("username").eq('id', user_id).execute()
        print(f"✅ UPDATE: {result.data[0]['username']}")
        
        # DELETE
        client.table('users').delete().eq('id', user_id).execute()
        result = client.table('users').select("*").eq('id', user_id).execute()
        if not result.data:
            print("✅ DELETE: ユーザー削除完了")
        
        print("\n🎉 CRUD操作テスト完了")
        return True
        
    except Exception as e:
        print(f"❌ CRUD操作エラー: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("📊 Instagram Analytics DB テスト")
    print("=" * 50)
    
    success = True
    
    # テスト実行
    success &= test_table_existence()
    success &= test_sample_data() 
    success &= test_crud_operations()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 B0102: テーブル作成テスト 全て成功!")
    else:
        print("❌ 一部テストが失敗しました")
    print("=" * 50)