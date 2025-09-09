# 01-me エンドポイント検証

## 🎯 検証目的
Instagram Graph APIの `/me` エンドポイントを使用して、現在認証されているユーザーの情報取得とInstagram Business Account IDの特定を行います。

## 📋 検証内容

### テスト1: 基本ユーザー情報取得
- **エンドポイント**: `/me`
- **取得データ**: ユーザーID、名前、メールアドレス
- **必要権限**: `instagram_basic`

### テスト2: 管理ページ・アカウント一覧
- **エンドポイント**: `/me/accounts`  
- **取得データ**: FacebookページとリンクされたInstagram Business Account情報
- **必要権限**: `pages_show_list`

## 🚀 実行方法

```bash
cd verification
source venv/bin/activate
python endpoint-tests/01-me/01-basic-user-info.py
```

## 📊 期待する結果

### 成功時
- ✅ ユーザー基本情報が取得される
- ✅ Instagram Business Account IDが特定される
- ✅ 次の検証ステップに進む準備完了

### 想定される問題
- ❌ **権限不足**: アプリの権限設定を確認
- ❌ **トークン期限切れ**: 新しいトークンを取得
- ⚠️ **Instagram未連携**: Facebook ManagerでInstagram連携

## 📁 出力ファイル
- `01-output-data.json`: 詳細な実行結果（JSON形式）
- このREADME更新（実行後）