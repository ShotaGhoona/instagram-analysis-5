# Instagram Analytics PoC

Instagram分析アプリのProof of Concept（概念実証）

## 🚀 クイックスタート

### 必要な環境
- Python 3.13+
- Node.js 18+
- Supabase アカウント

### 1. リポジトリクローン
```bash
git clone <repository-url>
cd instagram-analysis-5
```

### 2. バックエンド起動

```bash
# バックエンドディレクトリに移動
cd backend

# 仮想環境作成・アクティベート
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 必要最小限パッケージインストール
pip install supabase python-dotenv

# 環境変数設定
cp .env.example .env
# .envファイルを編集してSupabase認証情報を入力

# 接続テスト
python -c "from utils.supabase_client import supabase_client; print('✅ 接続成功' if supabase_client.client else '❌ 接続失敗')"

# データベーステスト（オプション）
python test_database.py
```

### 3. フロントエンド起動

```bash
# 新しいターミナルを開く
cd frontend

# 依存関係インストール
npm install

# 環境変数設定
cp .env.example .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 開発サーバー起動
npm run dev
```

### 4. アクセス確認
- **フロントエンド**: http://localhost:3000
- **バックエンド**: http://localhost:8000 (FastAPI起動後)

## 📁 プロジェクト構成

```
instagram-analysis-5/
├── README.md                 # このファイル
├── backend/                  # FastAPI バックエンド
│   ├── main.py              # FastAPI アプリ
│   ├── api/                 # API エンドポイント
│   ├── auth/                # 認証システム
│   ├── models/              # データベースモデル
│   ├── utils/               # ユーティリティ
│   ├── sql/                 # SQL スクリプト
│   └── .env                 # 環境変数（要設定）
├── frontend/                # Next.js フロントエンド
│   ├── src/app/            # App Router
│   ├── src/components/     # コンポーネント
│   ├── src/lib/            # ライブラリ
│   └── .env.local          # 環境変数（要設定）
├── docs/                   # 設計ドキュメント
│   ├── requirement-definition/
│   └── implementation-strategy/
└── verification/           # API検証スクリプト
```

## ⚙️ 環境設定

### バックエンド (.env)
```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

# Instagram API
INSTAGRAM_APP_ID=your-app-id
INSTAGRAM_APP_SECRET=your-app-secret
INSTAGRAM_ACCESS_TOKEN=your-access-token

# Authentication
SECRET_KEY=your-secret-key

# Environment
ENVIRONMENT=development
DEBUG=true
```

### フロントエンド (.env.local)
```bash
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Environment
NODE_ENV=development
```

## 🛠️ 開発コマンド

### バックエンド
```bash
cd backend
source venv/bin/activate

# データベーステスト
python test_database.py

# FastAPI開発サーバー起動（準備中）
# uvicorn main:app --reload
```

### フロントエンド
```bash
cd frontend

# 開発サーバー起動
npm run dev

# ビルド
npm run build

# リント
npm run lint
```

## 📋 開発状況

### 完了済み ✅
- Supabaseプロジェクト設定
- データベーステーブル作成（5テーブル）
- Next.js + shadcn/ui セットアップ
- プロジェクト構成・ドキュメント整備

### 進行中 🔄
- Instagram API統合
- FastAPI エンドポイント実装
- フロントエンド UI実装

### 全体進捗
- **バックエンド**: 35% → Instagram API統合が次のステップ
- **フロントエンド**: 30% → 各ページコンポーネント実装が次のステップ

詳細は [`docs/requirement-definition/21-completion-checklist.md`](docs/requirement-definition/21-completion-checklist.md) を参照

## 📚 ドキュメント

- [要件定義](docs/requirement-definition/) - 全体設計・要件
- [実装戦略](docs/implementation-strategy/) - タスク別実装ガイド
- [API検証結果](verification/) - Instagram API動作確認

## 🎯 PoC開発について

このプロジェクトはProof of Concept（概念実証）として開発中です：

- **目的**: Instagram分析機能の実現可能性検証
- **期間**: 約20日間の短期開発
- **品質**: 動作優先、完璧性より実用性重視
- **スコープ**: 100アカウント管理、1-3人利用想定

## 🔧 トラブルシューティング

### Python 3.13 + pydantic エラー
```bash
# 最小構成でインストール
pip install supabase python-dotenv
# 他のパッケージは必要時に個別インストール
```

### Supabase接続エラー
```bash
# 接続テスト実行
python -c "from utils.supabase_client import supabase_client; print('✅ 接続成功' if supabase_client.client else '❌ 接続失敗')"
```

### Next.js shadcn/ui設定
```bash
# components.jsonが存在することを確認
cat frontend/components.json
```

## 📧 サポート

プロジェクト固有の問題については：
- [実装チェックリスト](docs/requirement-definition/21-completion-checklist.md) で進捗確認
- [実装戦略ガイド](docs/implementation-strategy/README.md) で開発方針確認