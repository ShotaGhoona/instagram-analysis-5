# 03-account-info - アカウント基本情報検証

## 概要

毎日データ収集用のアカウント基本情報取得を検証します。

**検証エンドポイント:**
```
GET /{ig-user-id}?fields=id,username,name,profile_picture_url,followers_count,follows_count,media_count
```

## 検証スクリプト

### 01-basic-account-info.py
アカウント基本情報の取得テスト

**検証項目:**
- ユーザー名 (`username`)
- 表示名 (`name`)
- プロフィール画像URL (`profile_picture_url`)
- フォロワー数 (`followers_count`)
- フォロー数 (`follows_count`) 
- 投稿数 (`media_count`)
- 個別フィールドの可用性確認

**実行方法:**
```bash
cd verification
python endpoint-tests/03-account-info/01-basic-account-info.py
```

**前提条件:**
- `01-me/01-output-data.json` が存在すること（Page Access Token取得済み）

## 出力ファイル

- `01-output-data.json` - 検証結果データ