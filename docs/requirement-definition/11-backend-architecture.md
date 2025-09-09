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

## 🔧 FastAPIバックエンド構成（Clean Architecture）

### リファクタリング後ディレクトリ構造
```
backend/
├── main.py                      # FastAPI アプリ起点
├── requirements.txt
├──
├── api/                         # Presentation Layer
│   ├── __init__.py
│   ├── accounts.py             # アカウント管理API
│   ├── analytics.py            # 分析データAPI
│   ├── media.py                # 投稿データAPI
│   └── setup.py                # セットアップAPI
│
├── middleware/                  # Cross-cutting Concerns
│   ├── __init__.py
│   └── auth/                   # 認証・認可
│       ├── __init__.py
│       ├── README.md
│       └── simple_auth.py      # JWT認証実装
│
├── services/                    # Application Layer
│   ├── __init__.py
│   └── instagram_service.py    # Instagram関連ビジネスロジック
│
├── repositories/                # Infrastructure Layer
│   ├── __init__.py
│   ├── base.py                 # BaseRepository
│   ├── instagram_repository.py # Instagram データアクセス
│   └── user_repository.py      # ユーザーデータアクセス
│
├── external/                    # Infrastructure Layer
│   ├── __init__.py
│   └── instagram_client.py     # Instagram Graph API クライアント
│
├── core/                        # Core Infrastructure
│   ├── __init__.py
│   ├── config.py               # 設定管理（SUPABASE_ANON_KEY統一）
│   └── database.py             # データベース接続（統一クライアント）
│
├── models/                      # Domain Layer
│   ├── __init__.py
│   ├── user.py                 # ユーザーモデル
│   ├── instagram.py            # Instagramモデル
│   ├── analytics.py            # 分析モデル
│   └── sql/                    # Database Schema
│       ├── create_tables.sql   # テーブル作成SQL
│       └── sample_data.sql     # サンプルデータ
│
└── test/                        # Testing
    ├── collect_all_accounts_data.py
    ├── debug_insights_api.py
    ├── test_auth_api.py
    ├── test_b0203.py
    ├── test_b0204_multi_account.py
    ├── test_b0204.py
    ├── test_b0205_account_insights.py
    └── test_database.py
```

### Clean Architecture 各層の責任

#### 1. **Presentation Layer (api/)** - インターフェース層
- HTTPリクエスト/レスポンスの処理
- バリデーション
- Serviceの呼び出しのみ

#### 2. **Cross-cutting Concerns (middleware/)** - 横断的関心事
- 認証・認可（JWT Token管理）
- CORS処理
- エラーハンドリング統一
- ログ機能（将来実装予定）

#### 3. **Application Layer (services/)** - ビジネスロジック層
- 複雑なビジネスロジックの実装
- 複数のRepositoryの組み合わせ
- トランザクション管理

#### 4. **Infrastructure Layer** - インフラ層
- **repositories/**: データベースCRUD操作
- **external/**: Instagram API等の外部サービス連携
- **core/**: データベース接続・設定管理

#### 5. **Domain Layer (models/)** - エンティティ層
- Pydanticモデルの定義のみ
- ビジネスルールの表現
- データベーススキーマ（SQL）の管理

### Clean Architecture レイヤー図

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Routes (api/)                                      │
│  - accounts.py  - analytics.py  - media.py  - setup.py      │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                          │
├─────────────────────────────────────────────────────────────┤
│  Service Classes (services/)                                │
│  - instagram_service.py                                     │
│                                                             │
│  Cross-cutting Concerns (middleware/)                       │
│  - auth/simple_auth.py (認証・認可)                          │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                         │
├─────────────────────────────────────────────────────────────┤
│  Repository Pattern (repositories/)                         │
│  - base.py  - instagram_repository.py  - user_repository.py │
│                                                             │
│  External APIs (external/)                                  │
│  - instagram_client.py                                      │
│                                                             │
│  Database Connection (core/)                                │
│  - database.py  - config.py                                 │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   Domain Layer                               │
├─────────────────────────────────────────────────────────────┤
│  Domain Models (models/)                                    │
│  - user.py  - instagram.py  - analytics.py                  │
│  - sql/ (create_tables.sql, sample_data.sql)                │
└─────────────────────────────────────────────────────────────┘
```

### 依存関係の方向

Clean Architecture の原則に従い、依存関係は以下の方向に限定されます：

```
Presentation → Application → Infrastructure
      ↓            ↓
  Middleware → Domain
```

- **Presentation Layer** は Application Layer と Middleware に依存
- **Application Layer** は Infrastructure Layer と Domain Layer に依存  
- **Middleware** は Domain Layer に依存（横断的関心事）
- **Infrastructure Layer** は Domain Layer に依存
- **Domain Layer** は他の層に依存しない（最も内側）

### 主要な設計パターン

#### 1. Repository Pattern
データアクセスロジックを抽象化し、ドメインロジックからデータストレージの詳細を隠蔽

#### 2. Dependency Injection
FastAPI の依存関係注入を活用し、疎結合な設計を実現

#### 3. Service Layer Pattern
複雑なビジネスロジックを Service クラスに集約し、API層を薄く保つ

#### 4. Middleware Pattern
横断的関心事（認証・CORS・エラーハンドリング）をMiddleware層に分離

#### 5. DTO (Data Transfer Object)
API境界でのデータ転送にPydanticモデルを使用

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

## 🔄 リファクタリング戦略

## エラーハンドリング

### 階層別エラー処理
1. **Presentation Layer**: HTTP ステータスコードとエラーレスポンス
2. **Middleware Layer**: 横断的エラーハンドリング（統一レスポンス形式）
3. **Application Layer**: ビジネスロジックエラーの捕捉と変換
4. **Infrastructure Layer**: データベースエラーやAPI エラーの処理

### エラー種別（B0501対応予定）
- **400**: Bad Request（バリデーションエラー）
- **401**: Unauthorized（認証エラー）
- **403**: Forbidden（認可エラー）
- **404**: Not Found（リソース未存在）
- **500**: Internal Server Error（システムエラー）

### 統一エラーレスポンス形式
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力データが正しくありません",
    "details": {...}
  }
}
```

## 品質保証と保守性

### 保守性
- **単一責任の原則**: 各クラスの責務明確化
- **Clean Architecture**: 層間の明確な分離と依存関係制御
- **重複コード削除**: 統一されたデータベースクライアントと設定管理
- **テスタビリティ**: ユニットテスト・統合テスト対応
- **ドキュメント**: コメントとREADMEによる理解促進

### 拡張性
- **Middleware**: 新しい横断的関心事の追加が容易
- **Repository Pattern**: 新しいデータソースの追加が容易
- **Service Layer**: 新しいビジネスロジックの実装が容易

## アーキテクチャ改善履歴

### 2025-09-09: バックエンドリファクタリング実施
- **重複コード削除**: 302行のレガシーコード除去
- **認証アーキテクチャ改善**: `auth/` → `middleware/auth/` に移動
- **環境変数統一**: `SUPABASE_ANON_KEY`で統一
- **ファイル構造最適化**: テスト・SQLファイルの適切配置
- **Clean Architecture完全準拠**: 層間の明確な責務分離

### リファクタリング効果
- **コード品質**: 重複コード削除、一貫性向上
- **開発体験**: Import文の統一、テスト実行効率化
- **将来拡張**: エラーハンドリング、ログ機能等の追加基盤構築

## ⚡ PoCレベル最適化（リファクタリング後も維持）

### シンプル化項目
- **認証**: JWT使用、シンプルな実装
- **セキュリティ**: 基本的なバリデーションのみ
- **エラーハンドリング**: 基本的なログ出力のみ
- **キャッシュ**: なし（直接DB クエリ）
- **非同期処理**: 基本的な同期処理でスタート

### 技術選択理由
- **FastAPI**: 自動ドキュメント生成、型安全、依存注入サポート
- **Supabase**: PostgreSQL、リアルタイム機能（将来拡張可）
- **GitHub Actions**: 無料枠、簡単セットアップ
- **Clean Architecture**: 将来の拡張性を考慮した設計

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