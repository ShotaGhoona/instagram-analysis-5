# 認証モジュール (auth/)

## 概要
シンプルなJWT認証システムを実装

## ファイル
- `simple_auth.py` - 認証API + JWT トークン管理

## 主要機能
- ユーザー登録・ログイン
- JWT トークン生成・検証
- パスワードハッシュ化（bcrypt）
- 認証ミドルウェア

## API エンドポイント
```
POST /auth/register  # ユーザー登録
POST /auth/login     # ログイン
POST /auth/logout    # ログアウト
GET  /auth/me        # ユーザー情報取得
```

## 使用例
```python
from auth.simple_auth import get_current_user

@app.get("/protected")
async def protected_route(user = Depends(get_current_user)):
    return {"user": user.username}
```