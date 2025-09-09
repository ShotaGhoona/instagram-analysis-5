# Instagram Analytics Frontend

Instagram分析アプリのフロントエンド（Next.js + shadcn/ui + Recharts）

## セットアップ

### 1. 依存関係インストール

```bash
npm install
```

### 2. 環境変数設定

```bash
# .env.local ファイルを作成
cp .env.example .env.local

# バックエンドAPIのURL設定
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. 開発サーバー起動

```bash
npm run dev
```

## プロジェクト構成

### ページ構造（App Router）
```
/login                           # ログインページ
/analytics/account/[accountId]/
  ├── yearly                     # 年間分析ページ
  ├── monthly                    # 月間分析ページ
  └── posts                      # 投稿分析ページ
```

### コンポーネント構成
```
src/
├── components/
│   ├── layout/                  # レイアウトコンポーネント
│   ├── analytics/               # 分析関連コンポーネント
│   ├── filters/                 # フィルター関連コンポーネント
│   └── ui/                      # shadcn/ui コンポーネント
├── lib/
│   ├── api.ts                   # APIクライアント
│   ├── types.ts                 # TypeScript型定義
│   └── utils.ts                 # ユーティリティ関数
└── hooks/                       # カスタムフック
```

## 技術スタック

- **Next.js 14** - React フレームワーク（App Router）
- **TypeScript** - 型安全な開発
- **Tailwind CSS** - スタイリング
- **shadcn/ui** - UIコンポーネントライブラリ
- **Recharts** - データ可視化ライブラリ

## 主要機能

### 認証
- JWT認証システム
- ログイン・ログアウト機能

### 分析ダッシュボード
- 年間分析: フォロワー推移、エンゲージメント分析
- 月間分析: 日別統計、詳細グラフ
- 投稿分析: 個別投稿パフォーマンス、フィルター機能

### データ可視化
- Rechartsによるインタラクティブなグラフ
- レスポンシブデザイン対応

## 開発状況

✅ **完了済み**:
- Next.js + shadcn/ui セットアップ
- ディレクトリ構造作成
- APIクライアント実装
- 基本レイアウトコンポーネント
- TypeScript型定義
- 認証フック実装

🔄 **次のステップ**:
- 各ページコンポーネント実装
- データ可視化コンポーネント実装
- フィルター機能実装
- エラーハンドリング強化
- テストケース作成
