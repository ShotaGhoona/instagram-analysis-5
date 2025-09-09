-- サンプルデータ投入 (テスト用)

-- 1. テストユーザー作成 (パスワード: test123)
INSERT INTO users (username, password_hash) VALUES 
('test_user', '$2b$12$rXzF.0ycOdEYX6yq3cJBGOyV7mF8V0z0X4Nt6qFzQ8QzTtTcKwYqe'),
('demo_user', '$2b$12$rXzF.0ycOdEYX6yq3cJBGOyV7mF8V0z0X4Nt6qFzQ8QzTtTcKwYqe');

-- 2. テスト用Instagramアカウント (複数アカウント)
INSERT INTO instagram_accounts (name, ig_user_id, access_token, username, profile_picture_url) VALUES 
('メインアカウント', '17841455808057230', 'sample_access_token_1', 'main_account', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.2885-19/profile1.jpg'),
('サブアカウント', '17841455808057231', 'sample_access_token_2', 'sub_account', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.2885-19/profile2.jpg'),
('ビジネスアカウント', '17841455808057232', 'sample_access_token_3', 'business_account', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.2885-19/profile3.jpg');

-- 3. 日次アカウント統計サンプル (3つのアカウント × 最近7日分)
INSERT INTO daily_account_stats (date, ig_user_id, followers_count, follows_count, media_count, profile_views, website_clicks) VALUES 
-- メインアカウント
('2025-09-09', '17841455808057230', 1000, 500, 50, 100, 10),
('2025-09-08', '17841455808057230', 998, 500, 49, 95, 8),
('2025-09-07', '17841455808057230', 995, 499, 49, 110, 12),
('2025-09-06', '17841455808057230', 992, 499, 48, 88, 6),
('2025-09-05', '17841455808057230', 990, 498, 48, 102, 9),
('2025-09-04', '17841455808057230', 987, 498, 47, 75, 5),
('2025-09-03', '17841455808057230', 985, 497, 47, 92, 7),
-- サブアカウント
('2025-09-09', '17841455808057231', 750, 200, 30, 60, 3),
('2025-09-08', '17841455808057231', 748, 200, 30, 55, 2),
('2025-09-07', '17841455808057231', 745, 199, 29, 65, 4),
('2025-09-06', '17841455808057231', 743, 199, 29, 48, 1),
('2025-09-05', '17841455808057231', 741, 198, 28, 58, 3),
('2025-09-04', '17841455808057231', 739, 198, 28, 42, 2),
('2025-09-03', '17841455808057231', 737, 197, 27, 51, 2),
-- ビジネスアカウント
('2025-09-09', '17841455808057232', 2500, 150, 80, 200, 25),
('2025-09-08', '17841455808057232', 2495, 150, 79, 190, 22),
('2025-09-07', '17841455808057232', 2490, 149, 79, 210, 28),
('2025-09-06', '17841455808057232', 2485, 149, 78, 185, 20),
('2025-09-05', '17841455808057232', 2480, 148, 78, 195, 24),
('2025-09-04', '17841455808057232', 2475, 148, 77, 170, 18),
('2025-09-03', '17841455808057232', 2470, 147, 77, 180, 21);

-- 4. 投稿データサンプル (各アカウントの最近の投稿)
INSERT INTO media_posts (ig_media_id, ig_user_id, timestamp, media_type, caption, media_url, thumbnail_url, permalink) VALUES 
-- メインアカウント投稿
('18012345678901234', '17841455808057230', '2025-09-09 12:00:00', 'IMAGE', '今日の朝食🍳 #morning #breakfast', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/media1.jpg', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/thumb1.jpg', 'https://instagram.com/p/sample1'),
('18012345678901235', '17841455808057230', '2025-09-08 18:30:00', 'VIDEO', '夕日が綺麗でした🌅 #sunset #beautiful', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/media2.mp4', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/thumb2.jpg', 'https://instagram.com/p/sample2'),
('18012345678901236', '17841455808057230', '2025-09-07 14:15:00', 'CAROUSEL_ALBUM', '週末のお出かけ📸 #weekend #photography', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/media3.jpg', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/thumb3.jpg', 'https://instagram.com/p/sample3'),
-- サブアカウント投稿
('18012345678901237', '17841455808057231', '2025-09-09 10:00:00', 'IMAGE', 'カフェタイム☕️ #cafe #coffee', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/media4.jpg', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/thumb4.jpg', 'https://instagram.com/p/sample4'),
('18012345678901238', '17841455808057231', '2025-09-08 16:45:00', 'IMAGE', '読書中📚 #book #reading', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/media5.jpg', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/thumb5.jpg', 'https://instagram.com/p/sample5'),
-- ビジネスアカウント投稿
('18012345678901239', '17841455808057232', '2025-09-09 09:00:00', 'IMAGE', '新商品のお知らせ🎉 #newproduct #business', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/media6.jpg', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/thumb6.jpg', 'https://instagram.com/p/sample6'),
('18012345678901240', '17841455808057232', '2025-09-08 12:00:00', 'VIDEO', '商品紹介動画💼 #productintro #business', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/media7.mp4', 'https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/thumb7.jpg', 'https://instagram.com/p/sample7');

-- 5. 日次投稿統計サンプル (各投稿の統計データ)
INSERT INTO daily_media_stats (date, ig_media_id, like_count, comments_count, reach, views, shares, saved) VALUES 
-- メインアカウント投稿統計
('2025-09-09', '18012345678901234', 50, 5, 200, 150, 2, 8),
('2025-09-08', '18012345678901235', 75, 8, 300, 250, 4, 12),
('2025-09-07', '18012345678901236', 95, 12, 450, 380, 6, 18),
-- サブアカウント投稿統計  
('2025-09-09', '18012345678901237', 25, 2, 120, 90, 1, 4),
('2025-09-08', '18012345678901238', 35, 3, 150, 110, 2, 6),
-- ビジネスアカウント投稿統計
('2025-09-09', '18012345678901239', 120, 15, 800, 650, 8, 25),
('2025-09-08', '18012345678901240', 180, 22, 1200, 980, 12, 35);