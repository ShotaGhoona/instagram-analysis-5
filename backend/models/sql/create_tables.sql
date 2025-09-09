-- Instagram分析アプリ用テーブル作成 (PoC)
-- 作成日: 2025-09-09

-- 1. ユーザー管理テーブル
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Instagramアカウント管理テーブル
CREATE TABLE instagram_accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    ig_user_id VARCHAR(50) UNIQUE NOT NULL,
    access_token TEXT NOT NULL,
    username VARCHAR(100) NOT NULL,
    profile_picture_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 日次アカウント統計テーブル
CREATE TABLE daily_account_stats (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    ig_user_id VARCHAR(50) NOT NULL,
    followers_count INTEGER NOT NULL,
    follows_count INTEGER NOT NULL,
    media_count INTEGER NOT NULL,
    profile_views INTEGER,
    website_clicks INTEGER,
    UNIQUE(date, ig_user_id),
    FOREIGN KEY (ig_user_id) REFERENCES instagram_accounts(ig_user_id) ON DELETE CASCADE
);

-- 4. 投稿データテーブル
CREATE TABLE media_posts (
    id SERIAL PRIMARY KEY,
    ig_media_id VARCHAR(50) UNIQUE NOT NULL,
    ig_user_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    media_type VARCHAR(20) NOT NULL CHECK (media_type IN ('IMAGE', 'VIDEO', 'CAROUSEL_ALBUM')),
    caption TEXT,
    media_url TEXT NOT NULL,
    thumbnail_url TEXT,
    permalink TEXT NOT NULL,
    FOREIGN KEY (ig_user_id) REFERENCES instagram_accounts(ig_user_id) ON DELETE CASCADE
);

-- 5. 日次投稿統計テーブル
CREATE TABLE daily_media_stats (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    ig_media_id VARCHAR(50) NOT NULL,
    like_count INTEGER NOT NULL DEFAULT 0,
    comments_count INTEGER NOT NULL DEFAULT 0,
    reach INTEGER,
    views INTEGER,
    shares INTEGER,
    saved INTEGER,
    UNIQUE(date, ig_media_id),
    FOREIGN KEY (ig_media_id) REFERENCES media_posts(ig_media_id) ON DELETE CASCADE
);

-- インデックス作成 (最小限)
CREATE INDEX idx_daily_account_stats_date ON daily_account_stats(date);
CREATE INDEX idx_daily_media_stats_date ON daily_media_stats(date);
CREATE INDEX idx_media_posts_timestamp ON media_posts(timestamp);