# API ルート (api/)

## 概要
Instagram分析アプリの主要APIエンドポイント群

## ファイル構成
- `accounts.py` - Instagramアカウント管理
- `analytics.py` - 分析データ取得
- `media.py` - 投稿データ・インサイト

## 主要エンドポイント

### accounts.py
```
GET  /accounts/          # アカウント一覧
GET  /accounts/{id}      # 個別アカウント
POST /accounts/          # アカウント追加
```

### analytics.py  
```
GET /analytics/yearly/{account_id}   # 年間分析
GET /analytics/monthly/{account_id}  # 月間分析
GET /analytics/posts/{account_id}    # 投稿分析
```

### media.py
```
GET /media/{account_id}           # 投稿一覧
GET /media/{media_id}/insights    # インサイト
GET /media/stats/{account_id}     # 統計付き投稿
```

## 認証
全エンドポイントでJWT認証が必要