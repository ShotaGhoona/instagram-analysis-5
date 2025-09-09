# 毎日データ収集要件

## 収集データ一覧と対応エンドポイント

### アカウント基本情報（日1回）

| データ項目 | エンドポイント | 必須パラメータ | 頻度 | 検証状況 | 検証ファイル |
|-----------|-------------|------------|-----|---------|-------------|
| ユーザー名 | `/{ig-user-id}` | `fields=username` | 日1回 | 🎉 検証済み | `03-account-info/01-basic-account-info.py` |
| 表示名 | `/{ig-user-id}` | `fields=name` | 日1回 | 🎉 検証済み | `03-account-info/01-basic-account-info.py` |
| プロフィール画像 | `/{ig-user-id}` | `fields=profile_picture_url` | 日1回 | 🎉 検証済み | `03-account-info/01-basic-account-info.py` |
| フォロワー数 | `/{ig-user-id}` | `fields=followers_count` | 日1回 | 🎉 検証済み | `03-account-info/01-basic-account-info.py` |
| フォロー数 | `/{ig-user-id}` | `fields=follows_count` | 日1回 | 🎉 検証済み | `03-account-info/01-basic-account-info.py` |
| 投稿数 | `/{ig-user-id}` | `fields=media_count` | 日1回 | 🎉 検証済み | `03-account-info/01-basic-account-info.py` |

### 新規投稿データ（投稿毎）

| データ項目 | エンドポイント | 必須パラメータ | 頻度 | 検証状況 | 検証ファイル |
|-----------|-------------|------------|-----|---------|-------------|
| 投稿一覧 | `/{ig-user-id}/media` | `fields=id,timestamp,media_type,caption` | 日1回 | 🎉 検証済み | `04-media-posts/01-media-posts.py` |
| いいね数 | `/{ig-user-id}/media` | `fields=like_count` | 日1回 | 🎉 検証済み | `04-media-posts/01-media-posts.py` |
| コメント数 | `/{ig-user-id}/media` | `fields=comments_count` | 日1回 | 🎉 検証済み | `04-media-posts/01-media-posts.py` |
| サムネイル | `/{ig-user-id}/media` | `fields=media_url,thumbnail_url` | 日1回 | 🎉 検証済み | `04-media-posts/01-media-posts.py` |
| パーマリンク | `/{ig-user-id}/media` | `fields=permalink` | 日1回 | 🎉 検証済み | `04-media-posts/01-media-posts.py` |

### インサイトメトリクス（投稿毎）

| データ項目 | エンドポイント | 必須パラメータ | 頻度 | 検証状況 | 検証ファイル |
|-----------|-------------|------------|-----|---------|-------------|
| リーチ | `/{ig-media-id}/insights` | `metric=reach` | 日1回 | 🎉 検証済み | `05-media-insights/01-media-insights.py` |
| インプレッション | `/{ig-user-id}/insights` | `metric=impressions&period=day` | 日1回 | ❌ 未検証 | - |
| プロフィールアクセス | `/{ig-user-id}/insights` | `metric=profile_views&period=day` | 日1回 | ❌ 未検証 | - |
| ウェブサイトクリック | `/{ig-user-id}/insights` | `metric=website_clicks&period=day` | 日1回 | ❌ 未検証 | - |

### 動画視聴数メトリクス（全投稿タイプ対応）

| データ項目 | エンドポイント | 必須パラメータ | 頻度 | 検証状況 | 検証ファイル |
|-----------|-------------|------------|-----|---------|-------------|
| 動画視聴数（統一） | `/{ig-media-id}/insights` | `metric=views` | 日1回 | 🎉 **完全検証済み** | `05-media-insights/03-views-metric.py` |
| 動画視聴数（廃止） | `/{ig-media-id}/insights` | `metric=video_views` | - | ❌ **2025年4月廃止** | `05-media-insights/02-video-insights.py` |

## 収集フロー

### 1. アカウント基本情報更新 🎉 検証済み
```
GET /{ig-user-id}?fields=id,username,name,profile_picture_url,followers_count,follows_count,media_count
```

### 2. 新規投稿検出 🎉 検証済み
```
GET /{ig-user-id}/media?fields=id,timestamp,media_type,caption,like_count,comments_count,media_url,thumbnail_url,permalink&limit=25
```

### 3. 新規投稿のインサイト取得 🎉 完全検証済み
```
GET /{ig-media-id}/insights?metric=reach 🎉 検証済み
GET /{ig-media-id}/insights?metric=views 🎉 完全検証済み (統一メトリクス・全投稿タイプ対応)
GET /{ig-media-id}/insights?metric=video_views ❌ 廃止確認済み (2025年4月廃止)
```

### 4. アカウントレベルインサイト取得 ❌ 未検証
```
GET /{ig-user-id}/insights?metric=impressions,profile_views,website_clicks&period=day
```

## 保存データ構造

### daily_account_stats テーブル
- `date`: 収集日 🎉
- `ig_user_id`: Instagram User ID 🎉
- `username`: ユーザー名 🎉 
- `name`: 表示名 🎉
- `profile_picture_url`: プロフィール画像URL 🎉
- `followers_count`: フォロワー数 🎉
- `follows_count`: フォロー数 🎉
- `media_count`: 投稿数 🎉
- `impressions`: インプレッション数 ❌
- `profile_views`: プロフィールアクセス数 ❌
- `website_clicks`: ウェブサイトクリック数 ❌

### media_posts テーブル
- `ig_media_id`: Instagram Media ID 🎉
- `ig_user_id`: Instagram User ID 🎉
- `timestamp`: 投稿日時 🎉
- `media_type`: 投稿タイプ (IMAGE/VIDEO/CAROUSEL_ALBUM) 🎉
- `caption`: キャプション 🎉
- `media_url`: メディアURL 🎉
- `thumbnail_url`: サムネイルURL 🎉
- `permalink`: パーマリンク 🎉

### daily_media_stats テーブル  
- `date`: 収集日 📅
- `ig_media_id`: Instagram Media ID 🎉
- `like_count`: いいね数 🎉
- `comments_count`: コメント数 🎉
- `reach`: リーチ数 🎉
- `views`: 統一視聴数（全投稿タイプ対応） 🎉