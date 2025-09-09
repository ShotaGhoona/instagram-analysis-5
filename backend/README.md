# Instagram Analytics Backend

Instagram分析アプリのバックエンドAPI（FastAPI + Supabase）

## セットアップ

### 1. 環境構築

```bash
# Python仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係インストール
pip install -r requirements.txt
```

### 2. 環境変数設定

```bash
# .env ファイルを作成
cp .env.example .env

# 必要な環境変数を設定
# - SUPABASE_URL: SupabaseプロジェクトURL
# - SUPABASE_KEY: Supabaseのanon key
# - SECRET_KEY: JWT用の秘密鍵
```

### 3. データベース初期化

```python
# Python REPLまたはスクリプトで実行
from models.database import db_manager
await db_manager.create_tables()
```

### 4. 開発サーバー起動

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API仕様

### 認証 (`/auth`)

- `POST /auth/register` - ユーザー登録
- `POST /auth/login` - ログイン
- `POST /auth/logout` - ログアウト
- `GET /auth/me` - 現在のユーザー情報

### アカウント管理 (`/accounts`)

- `GET /accounts/` - Instagramアカウント一覧
- `GET /accounts/{account_id}` - 個別アカウント詳細
- `POST /accounts/` - 新規アカウント追加

### 分析データ (`/analytics`)

- `GET /analytics/yearly/{account_id}` - 年間分析データ
- `GET /analytics/monthly/{account_id}` - 月間分析データ
- `GET /analytics/posts/{account_id}` - 投稿分析データ

### 投稿データ (`/media`)

- `GET /media/{account_id}` - 投稿一覧
- `GET /media/{media_id}/insights` - 投稿インサイト
- `GET /media/stats/{account_id}` - 統計データ付き投稿一覧

## 技術構成

- **FastAPI**: Python Webフレームワーク
- **Supabase**: PostgreSQLデータベース + 認証
- **Pydantic**: データバリデーション
- **JWT**: 認証トークン
- **bcrypt**: パスワードハッシュ化

## データベーススキーマ

### テーブル構成
- `users` - ユーザー管理
- `instagram_accounts` - Instagramアカウント管理
- `daily_account_stats` - 日次アカウント統計
- `media_posts` - 投稿データ
- `daily_media_stats` - 日次投稿統計

## 開発状況

✅ **完了済み**:
- プロジェクト構造作成
- FastAPI基本設定
- Supabase接続設定
- 認証システム実装
- API ルート構造作成
- データベースモデル定義

🔄 **次のステップ**:
- データベース実際の実装とテスト
- Instagram API統合
- GitHub Actions データ収集
- エラーハンドリング強化
- テストケース作成