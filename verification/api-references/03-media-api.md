# 03. Instagram Graph API - メディア関連API

**最終更新**: 2025年01月09日  
**情報源**: Meta for Developers 公式ドキュメント  
**参照URL**: 
- [IG Media Object Reference](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-media)
- [IG User Media Endpoint](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media/)
- [IG Media Insights](https://developers.facebook.com/docs/instagram-api/reference/ig-media/insights/)

## 重要な2025年更新情報

### API移行期限
- **2025年4月21日**: レガシーエンドポイント完全廃止
- Instagram Media → **IG Media** オブジェクトへの移行が完了済み
- 新しいID フィールド（`ig_user_id`, `ig_media_id`, `ig_comment_id`）を使用

### 廃止されたフィールド
以下のフィールドは2025年に廃止されました：
- `filter_name`
- `location`
- `latitude`
- `longitude`

## IG Media オブジェクト仕様

### 基本情報
- **オブジェクトタイプ**: IG Media
- **Graph API バージョン**: v23.0（最新）
- **必要権限**: `instagram_business_basic`, `instagram_basic`
- **アカウント要件**: Instagram Business または Creator アカウント

### サポートされる操作

| 操作 | メソッド | サポート |
|------|----------|----------|
| 読み取り | GET | ✅ |
| 更新 | POST | ✅（コメント有効/無効のみ） |
| 作成 | POST | ❌ |
| 削除 | DELETE | ❌ |

## メディア取得エンドポイント

### ユーザーのメディア一覧取得
```
GET /<IG_USER_ID>/media
```

**制限事項:**
- 最新10,000件まで取得可能
- ストーリーは含まれない（別エンドポイントを使用）
- デフォルトではメディアIDのみ返却

**ページネーション:**
- `since`, `until` パラメータで時間範囲指定可能（Unix timestamp）

### 個別メディア情報取得
```
GET /<IG_MEDIA_ID>
```

## IG Media フィールド一覧

### 基本フィールド
| フィールド名 | データタイプ | 説明 |
|-------------|-------------|------|
| `id` | String | メディアの一意識別子 |
| `media_type` | Enum | `IMAGE`, `VIDEO`, `CAROUSEL_ALBUM` |
| `media_url` | String | メディアファイルの直接URL |
| `media_product_type` | Enum | `AD`, `FEED`, `STORY`, `REELS` |
| `caption` | String | メディアの説明文 |
| `timestamp` | Datetime | 作成日時（ISO 8601形式） |
| `permalink` | String | Instagram上での表示URL |
| `owner` | Object | メディア所有者情報 |

### エンゲージメントフィールド
| フィールド名 | データタイプ | 説明 |
|-------------|-------------|------|
| `like_count` | Integer | いいね数 |
| `comments_count` | Integer | コメント数 |

### メディアタイプ別対応

| フィールド | IMAGE | VIDEO | CAROUSEL | STORY | REELS |
|-----------|-------|-------|-----------|-------|-------|
| `media_url` | ✅ | ✅ | ❌ | ✅ | ✅ |
| `thumbnail_url` | ❌ | ✅ | ❌ | ❌ | ✅ |
| `like_count` | ✅ | ✅ | ✅ | ❌ | ✅ |
| `comments_count` | ✅ | ✅ | ✅ | ❌ | ✅ |

## エッジ（関連データ）

### children
カルーセル投稿の個別メディアを取得
```
GET /<CAROUSEL_MEDIA_ID>/children
```

### comments
メディアのコメント一覧を取得
```
GET /<IG_MEDIA_ID>/comments
```

### collaborators
共同作成者情報を取得
```
GET /<IG_MEDIA_ID>/collaborators
```

### insights
メディアのインサイトデータを取得
```
GET /<IG_MEDIA_ID>/insights
```

## Insights（インサイト）メトリクス

### 利用可能メトリクス一覧

| メトリクス名 | 説明 | 適用メディア |
|-------------|------|-------------|
| `comments` | コメント数 | Feed投稿, Reels |
| `follows` | フォロワー獲得数 | Feed投稿, Stories |
| `likes` | いいね数 | Feed投稿, Reels |
| `reach` | ユニークリーチ数 | Feed投稿, Reels, Stories |
| `saved` | 保存数 | Feed投稿, Reels |
| `shares` | シェア数 | Feed投稿, Reels, Stories |
| `total_interactions` | 総インタラクション数 | Feed投稿, Reels, Stories |
| `views` | 視聴数（2025年新メトリクス） | Feed投稿, Reels, Stories |
| `profile_visits` | プロフィール訪問数 | Feed投稿, Stories |
| `profile_activity` | プロフィールでのアクション数 | Feed投稿, Stories |

### Insights取得例
```
GET /<IG_MEDIA_ID>/insights?metric=reach,impressions,likes,comments,shares,saved,total_interactions,views
```

### Insights制限事項
- データ更新に最大48時間の遅延
- データ保持期間は最大2年
- オーガニックインタラクションのみカウント
- カルーセル内の個別メディアはInsights取得不可
- ストーリーのInsightsは24時間のみ利用可能

## リクエスト例

### 基本的なメディア情報取得
```bash
GET https://graph.instagram.com/v23.0/{media-id}?fields=id,media_type,media_url,caption,timestamp,like_count,comments_count&access_token={access-token}
```

### 詳細情報とInsights同時取得
```bash
GET https://graph.instagram.com/v23.0/{media-id}?fields=id,media_type,caption,timestamp,like_count,comments_count,insights.metric(reach,impressions,likes,saved,shares)&access_token={access-token}
```

### ユーザーのメディア一覧取得（フィールド指定）
```bash
GET https://graph.instagram.com/v23.0/{ig-user-id}/media?fields=id,media_type,caption,timestamp,like_count,comments_count&limit=25&access_token={access-token}
```

## レスポンス例

```json
{
  "id": "17895695668004550",
  "media_type": "IMAGE",
  "media_url": "https://scontent.cdninstagram.com/v/...",
  "caption": "投稿のキャプション文",
  "timestamp": "2025-01-09T10:30:00+0000",
  "like_count": 42,
  "comments_count": 3,
  "insights": {
    "data": [
      {
        "name": "reach",
        "period": "lifetime",
        "values": [{"value": 156}]
      },
      {
        "name": "impressions", 
        "period": "lifetime",
        "values": [{"value": 203}]
      }
    ]
  }
}
```

## 開発時の注意事項

1. **アクセス権限**: Business/Creatorアカウントのメディアのみアクセス可能
2. **レート制限**: Instagram Business Use Case rate limitingが適用
3. **データ遅延**: Insightsデータは最大48時間の遅延あり
4. **メディア制限**: ライブ動画は配信中のみアクセス可能
5. **ストーリー**: 専用エンドポイント `/stories` を使用

