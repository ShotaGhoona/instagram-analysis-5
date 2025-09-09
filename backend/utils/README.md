# ユーティリティ (utils/)

## 概要  
外部サービス接続とヘルパー関数

## ファイル
- `supabase_client.py` - Supabaseデータベース接続

## Supabaseクライアント
シングルトンパターンでSupabase接続を管理

### 機能
- 自動接続管理
- 接続テスト機能
- 環境変数からの設定読み込み

### 必要な環境変数
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

### 使用例
```python
from utils.supabase_client import supabase_client

# データベース操作
result = supabase_client.client.table('users').select('*').execute()

# 接続テスト
is_connected = await supabase_client.test_connection()
```

### 初期設定
1. `.env`ファイルに環境変数設定
2. Supabaseプロジェクト作成
3. テーブル作成後に利用開始