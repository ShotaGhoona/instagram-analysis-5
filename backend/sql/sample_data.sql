-- サンプルデータ投入 (テスト用)

-- 1. テストユーザー作成
INSERT INTO users (username, password_hash) VALUES 
('test_user', '$2b$12$sample.hash.for.testing.purposes.only');

-- 2. テスト用Instagramアカウント
INSERT INTO instagram_accounts (name, ig_user_id, access_token, username, profile_picture_url) VALUES 
('テストアカウント', '17841455808057230', 'sample_access_token', 'test_account', 'https://example.com/profile.jpg');

-- 3. 日次アカウント統計サンプル
INSERT INTO daily_account_stats (date, ig_user_id, followers_count, follows_count, media_count, profile_views, website_clicks) VALUES 
('2025-09-09', '17841455808057230', 1000, 500, 50, 100, 10);

-- 4. 投稿データサンプル
INSERT INTO media_posts (ig_media_id, ig_user_id, timestamp, media_type, caption, media_url, thumbnail_url, permalink) VALUES 
('18012345678901234', '17841455808057230', '2025-09-09 12:00:00', 'IMAGE', 'テスト投稿です', 'https://example.com/media.jpg', 'https://example.com/thumb.jpg', 'https://instagram.com/p/sample');

-- 5. 日次投稿統計サンプル
INSERT INTO daily_media_stats (date, ig_media_id, like_count, comments_count, reach, views, shares, saved) VALUES 
('2025-09-09', '18012345678901234', 50, 5, 200, 150, 2, 8);