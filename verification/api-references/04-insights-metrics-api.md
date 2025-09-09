# 04. Instagram Graph API - インサイト・メトリクス API

**最終更新**: 2025年01月09日  
**情報源**: Meta for Developers 公式ドキュメント  
**参照URL**: 
- [IG User Insights Reference](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/insights/)
- [Instagram Insights Overview](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/insights/)
- [Instagram Platform Reference](https://developers.facebook.com/docs/instagram-platform/reference/)

## 2025年重要更新情報

### 新機能と変更点
- **Views メトリクス**: 全メディアタイプ（Reels、Live、Photos、Carousels、Stories）で利用可能
- **プライバシー重視のレポート**: フォロワー数100未満のアカウントではフォロワーメトリクスが非表示
- **人口統計レポート**: 上位45のオーディエンスセグメントのみ表示
- **小規模アカウント制限**: フォロワー数が少ないアカウントでは一部メトリクスが制限

### API移行期限
- **2025年4月21日**: レガシーInsights エンドポイント廃止
- **Graph API v23.0**: 現在の最新バージョン

## インサイトAPI概要

Instagram Graph APIのインサイト機能は2つのレベルに分かれています：

1. **アカウントレベルインサイト**: IG User Insights
2. **メディアレベルインサイト**: IG Media Insights（別ドキュメント参照）

## IG User Insights（アカウントインサイト）

### 基本情報
- **エンドポイント**: `GET /<IG_USER_ID>/insights`
- **必要権限**: `instagram_basic`, `instagram_manage_insights`
- **アクセストークン**: User Access Token
- **アカウント要件**: Instagram Business または Creator アカウント

### 利用可能メトリクス

#### オーディエンス メトリクス
| メトリクス名 | 説明 | 期間 | 内訳データ |
|-------------|------|------|-----------|
| `audience_city` | フォロワーの都市別分布 | lifetime | 上位都市 |
| `audience_country` | フォロワーの国別分布 | lifetime | 上位国家 |
| `audience_gender_age` | フォロワーの性別・年齢分布 | lifetime | 性別×年齢層 |
| `audience_locale` | フォロワーの言語設定分布 | lifetime | 言語コード |
| `follower_count` | フォロワー数 | day | 日別推移 |

#### アクティビティ メトリクス
| メトリクス名 | 説明 | 期間 | 内訳データ |
|-------------|------|------|-----------|
| `impressions` | インプレッション総数 | day, week, days_28 | ソース別内訳 |
| `profile_views` | プロフィール閲覧数 | day, week, days_28 | - |
| `reach` | リーチ数 | day, week, days_28 | ソース別内訳 |
| `website_clicks` | ウェブサイトクリック数 | day, week, days_28 | - |
| `email_contacts` | メールコンタクト数 | day, week, days_28 | - |
| `phone_call_clicks` | 電話番号クリック数 | day, week, days_28 | - |
| `text_message_clicks` | SMS クリック数 | day, week, days_28 | - |
| `get_directions_clicks` | 道順クリック数 | day, week, days_28 | - |

#### 2025年新メトリクス
| メトリクス名 | 説明 | 期間 | 対応メディア |
|-------------|------|------|-------------|
| `total_value` | 総価値指標 | day, week, days_28 | 全メディア |
| `accounts_engaged` | エンゲージしたアカウント数 | day, week, days_28 | 全メディア |

### 時間期間指定

#### サポートされる期間
- **day**: 日別データ（最大93日間）
- **week**: 週別データ（最大104週間）
- **days_28**: 28日間の累計データ
- **lifetime**: アカウント作成からの累計データ

#### 期間指定パラメータ
```
since: 開始日（YYYY-MM-DD 形式）
until: 終了日（YYYY-MM-DD 形式）
period: day, week, days_28, lifetime
```

### 内訳データ（Breakdown）

#### インプレッション・リーチの内訳
```json
{
  "name": "impressions",
  "values": [
    {
      "value": 1547,
      "end_time": "2025-01-09T08:00:00+0000"
    }
  ],
  "title": "Impressions",
  "description": "Total number of times posts have been seen",
  "id": "instagram_user_id/insights/impressions/day"
}
```

#### オーディエンス分析の内訳
```json
{
  "name": "audience_city",
  "period": "lifetime", 
  "values": [
    {
      "value": {
        "Tokyo, Japan": 156,
        "Osaka, Japan": 89,
        "New York, NY": 67
      }
    }
  ]
}
```

## リクエスト例

### 基本的なアカウントインサイト取得
```bash
GET https://graph.instagram.com/v23.0/{ig-user-id}/insights
  ?metric=impressions,reach,profile_views,website_clicks,follower_count
  &period=day
  &since=2025-01-01
  &until=2025-01-07
  &access_token={access-token}
```

### オーディエンス情報取得
```bash
GET https://graph.instagram.com/v23.0/{ig-user-id}/insights
  ?metric=audience_gender_age,audience_city,audience_country
  &period=lifetime
  &access_token={access-token}
```

### 週別データ取得
```bash
GET https://graph.instagram.com/v23.0/{ig-user-id}/insights
  ?metric=impressions,reach,profile_views
  &period=week
  &since=2025-01-01
  &until=2025-01-31
  &access_token={access-token}
```

## レスポンス例

### 日別インサイトデータ
```json
{
  "data": [
    {
      "name": "impressions",
      "period": "day",
      "values": [
        {
          "value": 2407,
          "end_time": "2025-01-08T08:00:00+0000"
        },
        {
          "value": 1837,
          "end_time": "2025-01-09T08:00:00+0000"
        }
      ],
      "title": "Impressions",
      "description": "Total number of times posts have been seen"
    },
    {
      "name": "reach", 
      "period": "day",
      "values": [
        {
          "value": 1205,
          "end_time": "2025-01-08T08:00:00+0000"
        }
      ]
    }
  ]
}
```

### オーディエンス分析データ
```json
{
  "data": [
    {
      "name": "audience_gender_age",
      "period": "lifetime",
      "values": [
        {
          "value": {
            "M.25-34": 45,
            "F.25-34": 38,
            "M.18-24": 23,
            "F.18-24": 19
          }
        }
      ],
      "title": "Audience Gender and Age",
      "description": "Gender and age distribution of followers"
    }
  ]
}
```

## 制限事項と注意点

### データ更新頻度
- **リアルタイムデータ**: フォロワー数など一部メトリクス
- **24時間遅延**: インプレッション、リーチなど大部分のメトリクス
- **48時間遅延**: 詳細なエンゲージメントデータ

### アクセス制限
- **小規模アカウント**: フォロワー100未満でフォロワーメトリクス制限
- **プライバシー保護**: 個人を特定できるデータは除外
- **地域制限**: 一部地域では利用不可の機能あり

### データ保持期間
- **日別データ**: 最大93日
- **週別データ**: 最大2年間
- **28日間データ**: 最大1年間
- **ライフタイムデータ**: アカウント削除まで

### レート制限
- **Instagram Business Use Case**: 4800 × インプレッション数 / 24時間
- **Platform Rate Limiting**: ビジネス発見とハッシュタグ検索のみ

## エラー処理

### よくあるエラー
```json
{
  "error": {
    "message": "Insufficient permissions",
    "type": "OAuthException",
    "code": 10
  }
}
```

### エラー対応
- **権限不足**: `instagram_manage_insights` 権限を確認
- **期間エラー**: since/until パラメータの形式を確認
- **アカウントタイプエラー**: Business/Creator アカウントに変更


## 開発時のベストプラクティス

1. **バッチ処理**: 複数メトリクスを1回のリクエストで取得
2. **キャッシング**: ライフタイムデータは適切にキャッシュ
3. **エラーハンドリング**: 権限エラーとデータ不足の適切な処理
4. **レート制限対応**: リクエスト間隔の調整
5. **データ検証**: 返却データの妥当性チェック