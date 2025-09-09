# 06. Instagram Graph API - エンドポイント一覧

**最終更新**: 2025年01月09日  
**Graph API バージョン**: v23.0

## 基本URL

| 認証方式 | ベースURL |
|----------|-----------|
| Facebook Login for Business | `https://graph.facebook.com/v23.0/` |
| Business Login for Instagram | `https://graph.instagram.com/` |

## 主要エンドポイント一覧

### ユーザー・アカウント関連

| エンドポイント | メソッド | 説明 | 必要権限 | 用途 |
|---------------|----------|------|----------|------|
| `/me` | GET | 現在のユーザー情報 | `instagram_basic` | アカウント基本情報 |
| `/me/accounts` | GET | 管理ページ一覧 | `pages_show_list` | Instagram Business Account ID取得 |
| `/{ig-user-id}` | GET | IG User情報 | `instagram_basic` | プロフィール詳細 |

### メディア関連

| エンドポイント | メソッド | 説明 | 必要権限 | 用途 |
|---------------|----------|------|----------|------|
| `/{ig-user-id}/media` | GET | メディア一覧 | `instagram_basic` | **投稿分析ページ** |
| `/{ig-media-id}` | GET | 個別メディア詳細 | `instagram_basic` | 投稿詳細情報 |
| `/{ig-media-id}/children` | GET | カルーセル子要素 | `instagram_basic` | カルーセル投稿 |

### インサイト関連

| エンドポイント | メソッド | 説明 | 必要権限 | 用途 |
|---------------|----------|------|----------|------|
| `/{ig-user-id}/insights` | GET | アカウントインサイト | `instagram_manage_insights` | **年間・月間分析** |
| `/{ig-media-id}/insights` | GET | メディアインサイト | `instagram_manage_insights` | **投稿分析ページ** |

### 認証関連

| エンドポイント | メソッド | 説明 | パラメータ | 用途 |
|---------------|----------|------|-----------|------|
| `/oauth/access_token` | POST | 短期トークン取得 | `code`, `client_id`, `client_secret` | 初回認証 |
| `/oauth/access_token` | GET | 長期トークン交換 | `grant_type=fb_exchange_token` | トークン長期化 |
| `/refresh_access_token` | GET | トークンリフレッシュ | `access_token` | トークン更新 |

## 重要パラメータ

### フィールド指定
```
fields=id,media_type,caption,timestamp,like_count,comments_count
```

### インサイトメトリクス
```
metric=reach,impressions,likes,saved,shares,views
```

### 期間指定
```
period=day,week,days_28,lifetime
since=2025-01-01&until=2025-01-31
```

## レート制限

- **Instagram Business Use Case**: `4800 × インプレッション数 / 24時間`
- **Platform Rate Limiting**: ビジネス発見・ハッシュタグ検索のみ