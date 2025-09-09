# 06-account-insights - アカウントレベルインサイト検証

## 概要

毎日のデータ収集に必要なアカウントレベルインサイトメトリクスの取得を検証します。

**検証エンドポイント:**
```
GET /{ig-user-id}/insights?metric=profile_views,website_clicks&period=day&metric_type=total_value
```

## 検証スクリプト

### 01-account-insights.py 🔑
アカウントレベルインサイトの取得テスト（長期トークン対応済み）

**検証項目:**
- プロフィールアクセス数 (`metric=profile_views&period=day&metric_type=total_value`)  
- ウェブサイトクリック数 (`metric=website_clicks&period=day&metric_type=total_value`)
- 複数メトリクス一括取得テスト
- 個別メトリクス取得テスト
- 期間パラメータ検証

**重要**: `profile_views`, `website_clicks` メトリクスには `metric_type=total_value` パラメータが必須です。

**実行方法:**
```bash
cd verification
python endpoint-tests/06-account-insights/01-account-insights.py
```

**前提条件:**
- `01-me/01-output-data.json` が存在すること
- `02-refresh_access_token/01-output-data.json` が存在すること（長期トークン）
- Instagram Business Accountにinsights権限が設定されていること

## 期待する結果

### プロフィールアクセス数メトリクス
- 日次プロフィールビュー数の取得成功
- プロフィールページアクセス数値

### ウェブサイトクリック数メトリクス
- 日次ウェブサイトクリック数の取得成功
- プロフィール内リンククリック数値

## 検証パターン

### テスト1: 複数メトリクス一括取得
```
GET /{ig-user-id}/insights?metric=profile_views,website_clicks&period=day&metric_type=total_value
```

### テスト2: 個別メトリクス取得
```
GET /{ig-user-id}/insights?metric=profile_views&period=day&metric_type=total_value
GET /{ig-user-id}/insights?metric=website_clicks&period=day&metric_type=total_value
```

### テスト3: 期間パラメータ検証
```
GET /{ig-user-id}/insights?metric=profile_views&period=day&metric_type=total_value
```

## 出力ファイル

- `01-output-data.json` - アカウントインサイト検証結果

## 注意事項

- アカウントレベルインサイトは`period=day`パラメータが必須
- データは過去24時間の集計値として提供される
- 権限不足の場合は空のデータまたはエラーが返される可能性がある
- 新しいアカウントではデータが不足している場合がある