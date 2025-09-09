# 04-media-posts - 投稿データ検証

## 概要

毎日データ収集用の投稿データ取得を検証します。

**検証エンドポイント:**
```
GET /{ig-user-id}/media?fields=id,timestamp,media_type,caption,like_count,comments_count,media_url,thumbnail_url,permalink&limit=25
```

## 検証スクリプト

### 01-media-posts.py
投稿データの一括取得テスト

**検証項目:**
- 投稿ID (`id`)
- 投稿日時 (`timestamp`)
- 投稿タイプ (`media_type`)
- キャプション (`caption`)
- いいね数 (`like_count`)
- コメント数 (`comments_count`)
- メディアURL (`media_url`)
- サムネイルURL (`thumbnail_url`)
- パーマリンク (`permalink`)
- 個別フィールドの可用性確認

**実行方法:**
```bash
cd verification
python endpoint-tests/04-media-posts/01-media-posts.py
```

**前提条件:**
- `01-me/01-output-data.json` が存在すること（Page Access Token取得済み）

## 出力ファイル

- `01-output-data.json` - 検証結果データ