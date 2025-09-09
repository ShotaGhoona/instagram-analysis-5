# Instagram Analytics ER図

## データベース構成

Instagram分析アプリのデータベース構造を以下に示します。GitHub Actionsによる自動データ収集を前提とした設計です。

### テーブル一覧

1. **users** - アプリケーションユーザー管理
2. **instagram_accounts** - Instagram Business Accountsの管理
3. **daily_account_stats** - アカウント統計の日次データ
4. **media_posts** - Instagram投稿データ
5. **daily_media_stats** - 投稿統計の日次データ

---

## ER図 (ASCII形式)

```
┌─────────────────┐       ┌─────────────────────┐       ┌──────────────────────┐
│     users       │       │  instagram_accounts │       │  daily_account_stats │
├─────────────────┤       ├─────────────────────┤       ├──────────────────────┤
│ id (PK)         │       │ id (PK)             │   ┌───│ id (PK)              │
│ username (UNIQ) │       │ name                │   │   │ date                 │
│ password_hash   │       │ ig_user_id (UNIQ)   │───┤   │ ig_user_id (FK)      │
│ created_at      │       │ access_token        │   │   │ followers_count      │
└─────────────────┘       │ username            │   │   │ follows_count        │
                          │ profile_picture_url │   │   │ media_count          │
                          │ created_at          │   │   │ profile_views        │
                          └─────────────────────┘   │   │ website_clicks       │
                                    │               │   │ UNIQUE(date, ig_user_id) │
                                    │               │   └──────────────────────┘
                                    │               │
                                    │               │   ┌──────────────────────┐
                                    │               └───│  daily_media_stats   │
                                    │                   ├──────────────────────┤
                                    │               ┌───│ id (PK)              │
                                    │               │   │ date                 │
                                    │               │   │ ig_media_id (FK)     │
                                    │               │   │ like_count           │
                                    │               │   │ comments_count       │
                                    │               │   │ reach                │
                                    │               │   │ views                │
                                    │               │   │ shares               │
                                    │               │   │ saved                │
                                    │               │   │ UNIQUE(date, ig_media_id) │
                                    │               │   └──────────────────────┘
                                    │               │
                          ┌─────────────────────┐   │
                          │    media_posts      │───┘
                          ├─────────────────────┤
                          │ id (PK)             │
                          │ ig_media_id (UNIQ)  │
                          │ ig_user_id (FK)     │
                          │ timestamp           │
                          │ media_type          │
                          │ caption             │
                          │ media_url           │
                          │ thumbnail_url       │
                          │ permalink           │
                          └─────────────────────┘
```

---

## テーブル詳細

### 1. users
アプリケーション認証用のユーザーテーブル
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. instagram_accounts
Instagram Business Accountsの基本情報とアクセストークンを管理
```sql
CREATE TABLE instagram_accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,                -- Page名
    ig_user_id VARCHAR(50) UNIQUE NOT NULL,    -- Instagram User ID
    access_token TEXT NOT NULL,                -- 長期アクセストークン
    username VARCHAR(100) NOT NULL,            -- @username
    profile_picture_url TEXT,                  -- プロフィール画像URL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. daily_account_stats
アカウントレベルの統計を日次で保存（GitHub Actions収集対象）
```sql
CREATE TABLE daily_account_stats (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    ig_user_id VARCHAR(50) NOT NULL,           -- FK to instagram_accounts
    followers_count INTEGER NOT NULL,          -- フォロワー数
    follows_count INTEGER NOT NULL,            -- フォロー数
    media_count INTEGER NOT NULL,              -- 投稿数
    profile_views INTEGER,                     -- プロフィール閲覧数
    website_clicks INTEGER,                    -- ウェブサイトクリック数
    UNIQUE(date, ig_user_id),
    FOREIGN KEY (ig_user_id) REFERENCES instagram_accounts(ig_user_id)
);
```

### 4. media_posts
Instagram投稿の基本情報を保存
```sql
CREATE TABLE media_posts (
    id SERIAL PRIMARY KEY,
    ig_media_id VARCHAR(50) UNIQUE NOT NULL,   -- Instagram Media ID
    ig_user_id VARCHAR(50) NOT NULL,           -- FK to instagram_accounts
    timestamp TIMESTAMP NOT NULL,              -- 投稿日時
    media_type VARCHAR(20) NOT NULL,           -- IMAGE, VIDEO, CAROUSEL_ALBUM
    caption TEXT,                              -- キャプション
    media_url TEXT NOT NULL,                   -- メディアURL
    thumbnail_url TEXT,                        -- サムネイルURL (動画用)
    permalink TEXT NOT NULL,                   -- Instagram投稿URL
    FOREIGN KEY (ig_user_id) REFERENCES instagram_accounts(ig_user_id)
);
```

### 5. daily_media_stats
投稿レベルの統計を日次で保存（GitHub Actions収集対象）
```sql
CREATE TABLE daily_media_stats (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    ig_media_id VARCHAR(50) NOT NULL,          -- FK to media_posts
    like_count INTEGER NOT NULL,               -- いいね数
    comments_count INTEGER NOT NULL,           -- コメント数
    reach INTEGER,                             -- リーチ数
    views INTEGER,                             -- 動画再生数
    shares INTEGER,                            -- シェア数
    saved INTEGER,                             -- 保存数
    UNIQUE(date, ig_media_id),
    FOREIGN KEY (ig_media_id) REFERENCES media_posts(ig_media_id)
);
```

---

## GitHub Actions データ収集仕様

### 日次データ収集対象

#### 1. アカウント基本情報 (daily_account_stats)
- **API**: `GET /{ig-user-id}?fields=followers_count,follows_count,media_count`
- **頻度**: 毎日 1回（例：午前 9:00 JST）
- **データ**: フォロワー数、フォロー数、投稿数の推移

#### 2. アカウントインサイト (daily_account_stats)
- **API**: `GET /{ig-user-id}/insights?metric=profile_views,website_clicks&period=day`
- **頻度**: 毎日 1回
- **データ**: プロフィール閲覧数、ウェブサイトクリック数

#### 3. 投稿一覧 (media_posts)
- **API**: `GET /{ig-user-id}/media?fields=id,timestamp,media_type,caption,media_url,thumbnail_url,permalink`
- **頻度**: 毎日 1回（新規投稿の検出）
- **データ**: 新規投稿の基本情報

#### 4. 投稿インサイト (daily_media_stats)
- **API**: `GET /{ig-media-id}/insights?metric=reach,impressions,likes,comments,saves,shares`
- **頻度**: 毎日 1回（既存全投稿対象）
- **データ**: 各投稿のパフォーマンス統計

### データ更新フロー
1. **アカウント情報更新**: 基本統計 + インサイトの取得・保存
2. **新規投稿検出**: 最新投稿をチェック、新規があれば `media_posts` に追加
3. **投稿統計更新**: 全投稿のインサイトを取得して `daily_media_stats` に保存
4. **エラーハンドリング**: API制限・トークン期限切れ等の対応

---

## インデックス推奨設定

```sql
-- パフォーマンス向上のためのインデックス
CREATE INDEX idx_daily_account_stats_date_user ON daily_account_stats(date, ig_user_id);
CREATE INDEX idx_daily_media_stats_date_media ON daily_media_stats(date, ig_media_id);
CREATE INDEX idx_media_posts_user_timestamp ON media_posts(ig_user_id, timestamp DESC);
```

---

## データ保持ポリシー

- **アカウント統計**: 無制限（分析のため全履歴保持）
- **投稿データ**: 無制限（コンテンツ分析のため）
- **投稿統計**: 無制限（パフォーマンス分析のため）
- **アクセストークン**: 60日間有効（自動更新機能で管理）

このER図に基づいて、GitHub Actionsでの自動データ収集システムを構築します。