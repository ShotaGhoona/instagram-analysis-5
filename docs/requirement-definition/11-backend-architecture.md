# バックエンドアーキテクチャ設計

**プロジェクト**: Instagram分析アプリ（PoC）  
**対象**: 1-3人、100Instagramアカウント管理  
**スタック**: FastAPI + Supabase + Next.js

## 🏗️ システム全体構成

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Next.js       │────│   FastAPI    │────│   Supabase      │
│   (Frontend)    │    │  (Backend)   │    │  (Database)     │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │
                              │
                    ┌─────────────────┐
                    │ GitHub Actions  │
                    │ (Data Collector)│
                    └─────────────────┘
                              │
                              │
                    ┌─────────────────┐
                    │Instagram Graph  │
                    │      API        │
                    └─────────────────┘
```

## 📊 データベース設計（Supabase）

### テーブル構造
```sql
-- ユーザー管理（超シンプル）
users (id, username, password_hash, created_at)

-- Instagramアカウント管理
instagram_accounts (
  id, name, ig_user_id, access_token, 
  username, profile_picture_url, created_at
)

-- 日次アカウント統計
daily_account_stats (
  date, ig_user_id, followers_count, follows_count, 
  media_count, profile_views, website_clicks
)

-- 投稿データ
media_posts (
  ig_media_id, ig_user_id, timestamp, media_type,
  caption, media_url, thumbnail_url, permalink
)

-- 日次投稿統計
daily_media_stats (
  date, ig_media_id, like_count, comments_count,
  reach, views, shares, saved
)
```

## 🔧 FastAPIバックエンド構成

### ディレクトリ構造
```
backend/
├── main.py              # FastAPI アプリ起点
├── auth/
│   ├── __init__.py
│   └── simple_auth.py   # シンプル認証
├── api/
│   ├── __init__.py
│   ├── accounts.py      # アカウント管理API
│   ├── analytics.py     # 分析データAPI
│   ├── media.py         # 投稿データAPI
│   └── setup.py         # セットアップ・トークン管理API
├── models/
│   ├── __init__.py
│   └── database.py      # Supabaseモデル
└── utils/
    ├── __init__.py
    ├── supabase_client.py # Supabase接続
    └── instagram_client.py # Instagram API統合
```

### 主要API エンドポイント
```python
# 認証
POST /auth/login
POST /auth/logout

# セットアップ（トークン管理）
POST /setup/refresh-tokens    # 全アカウントのトークンリフレッシュ・新規追加

# アカウント管理
GET  /accounts          # 全Instagramアカウント一覧
GET  /accounts/{id}     # 個別アカウント詳細

# 分析データ
GET  /analytics/yearly/{account_id}   # 年間分析
GET  /analytics/monthly/{account_id}  # 月間分析  
GET  /analytics/posts/{account_id}    # 投稿分析

# 投稿データ
GET  /media/{account_id}              # 投稿一覧
GET  /media/{media_id}/insights       # 投稿インサイト
```

## 🤖 GitHub Actions データ収集

### ワークフロー構成
```yaml
# .github/workflows/data-collection.yml
name: Daily Instagram Data Collection
on:
  schedule:
    - cron: '0 9 * * *'  # 毎日9時実行

jobs:
  collect:
    runs-on: ubuntu-latest
    steps:
      - name: データ収集スクリプト実行
        run: python scripts/daily_collector.py
      - name: Supabaseへデータ保存
        run: python scripts/save_to_database.py
```

### データ収集フロー
1. **アカウント基本情報更新** (日1回)
2. **新規投稿検出・保存** (投稿毎)
3. **投稿インサイト取得** (投稿毎)
4. **アカウントレベルインサイト取得** (日1回)

## 🎯 実装優先度

### Phase 1: 基盤構築
1. ✅ **Supabase セットアップ**
2. ✅ **FastAPI 基本構成**
3. ✅ **シンプル認証実装**
4. ✅ **データベース初期化**

### Phase 2: データ収集
1. ✅ **GitHub Actions セットアップ**
2. ✅ **Instagram API 統合**
3. ✅ **毎日データ収集自動化**

### Phase 3: 分析API
1. ✅ **投稿分析エンドポイント**
2. ✅ **年間/月間分析エンドポイント**
3. ✅ **アカウント管理エンドポイント**

## ⚡ PoCレベル最適化

### シンプル化項目
- **認証**: JWT不使用、セッションベース
- **セキュリティ**: RLS無効、基本的なバリデーションのみ
- **エラーハンドリング**: 基本的なログ出力のみ
- **キャッシュ**: なし（直接DB クエリ）
- **非同期処理**: 基本的な同期処理でスタート

### 技術選択理由
- **FastAPI**: 自動ドキュメント生成、型安全
- **Supabase**: PostgreSQL、リアルタイム機能（将来拡張可）
- **GitHub Actions**: 無料枠、簡単セットアップ

## 🚀 デプロイ戦略

### 開発環境
- **Backend**: `uvicorn main:app --reload`
- **Frontend**: `npm run dev`
- **Database**: Supabase クラウド

### 本番環境（PoC）
- **Backend**: Vercel / Railway
- **Frontend**: Vercel
- **Database**: Supabase 本番環境

**実装時間見積**: Backend 3-5日、データ収集 2-3日、テスト・統合 1-2日