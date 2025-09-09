# 05. Instagram Graph API - 認証・トークン管理

**最終更新**: 2025年01月09日  
**情報源**: Meta for Developers 公式ドキュメント  
**参照URL**: 
- [Instagram Platform Getting Started](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/getting-started)
- [Facebook Login for Business](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/)
- [Permissions Reference](https://developers.facebook.com/docs/permissions/reference)
- [Instagram Platform Authentication](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/getting-started)

## 2025年認証システム概要

### 認証方式の選択

Instagram Graph API では2つの認証方式が利用可能です：

| 認証方式 | ログイン方法 | 対象アカウント | ベースURL |
|----------|-------------|---------------|-----------|
| **Facebook Login for Business** | Facebook認証情報 | Facebook PageにリンクされたInstagram Business/Creator | `graph.facebook.com` |
| **Business Login for Instagram** | Instagram認証情報 | Instagram Business/Creator（単体） | `graph.instagram.com` |

### 推奨認証方式

**Facebook Login for Business** を推奨：
- より多くの機能にアクセス可能（ハッシュタグ検索、商品タグ付け等）
- 安定したAPI提供
- 豊富なInsights データ

## アプリセットアップ

### 1. Meta App Dashboard での設定

#### 必要な製品追加
```
Facebook Login for Business の場合:
✅ Facebook Login for Business
✅ Instagram > Instagram API setup with Facebook login
✅ Messenger（メッセージング機能使用時）

Business Login for Instagram の場合:
✅ Instagram > Instagram API setup with Instagram login
```

#### アプリID の取得
- **Facebook Login**: Meta App Dashboard 上部のApp ID
- **Instagram Login**: Instagram > API setup with Instagram login セクションのInstagram App ID

### 2. 開発環境設定

#### リダイレクトURI設定
```
開発環境: http://localhost:3000/auth/callback
本番環境: https://yourdomain.com/auth/callback
```

#### ドメイン検証
本番環境では以下の設定が必要：
- App Domains の設定
- Privacy Policy URL
- Terms of Service URL

## 権限（Permissions）一覧

### Facebook Login for Business 権限

| 権限名 | 説明 | 用途 | レビュー要否 |
|--------|------|------|-------------|
| `instagram_basic` | 基本的なプロフィール・メディア情報 | プロフィール情報、メディア一覧取得 | Standard Accessで利用可能 |
| `instagram_content_publish` | メディア投稿権限 | 投稿作成・公開 | App Review必要 |
| `instagram_manage_comments` | コメント管理権限 | コメント取得・返信・削除 | App Review必要 |
| `instagram_manage_insights` | インサイトデータアクセス | アナリティクス データ取得 | App Review必要 |
| `instagram_manage_messages` | メッセージング権限 | DM送受信 | App Review必要 |
| `pages_show_list` | Facebookページ一覧 | リンクされたページ情報取得 | Standard Accessで利用可能 |
| `pages_read_engagement` | ページエンゲージメント | ページ関連データ取得 | App Review必要 |

### Business Login for Instagram 権限

| 権限名 | 説明 | 用途 | レビュー要否 |
|--------|------|------|-------------|
| `instagram_business_basic` | Instagram基本アクセス | プロフィール・メディア取得 | Standard Accessで利用可能 |
| `instagram_business_content_publish` | コンテンツ投稿 | メディア投稿・公開 | App Review必要 |
| `instagram_business_manage_comments` | コメント管理 | コメント操作 | App Review必要 |
| `instagram_business_manage_messages` | メッセージ管理 | DM管理 | App Review必要 |

### 我々のアプリに必要な権限

```
最小構成（PoC）:
✅ instagram_basic
✅ instagram_manage_insights
✅ pages_show_list（Facebook Login使用時）

完全版:
✅ instagram_basic
✅ instagram_manage_insights  
✅ instagram_manage_comments
✅ pages_show_list
✅ pages_read_engagement
```

## アクセストークン管理

### トークンタイプ

| トークンタイプ | 有効期間 | 用途 | 取得方法 |
|---------------|----------|------|----------|
| **短期トークン** | 1時間 | 初期認証 | 認証フロー完了時 |
| **長期トークン** | 60日間 | API呼び出し | 短期トークンから交換 |
| **リフレッシュトークン** | - | トークン更新 | 長期トークンと同時取得 |

### 認証フロー

#### 1. 認証URL生成
```
Facebook Login の場合:
https://www.facebook.com/v23.0/dialog/oauth?
  client_id={app-id}
  &redirect_uri={redirect-uri}
  &scope=instagram_basic,instagram_manage_insights,pages_show_list
  &response_type=code
  &state={state-param}

Instagram Login の場合:
https://api.instagram.com/oauth/authorize?
  client_id={instagram-app-id}
  &redirect_uri={redirect-uri}
  &scope=instagram_business_basic,instagram_business_manage_insights
  &response_type=code
```

#### 2. 認証コード取得
ユーザー認証後、リダイレクトURIに以下の形式で返却：
```
https://yourdomain.com/auth/callback?code={authorization-code}&state={state-param}
```

#### 3. 短期アクセストークン取得
```bash
POST https://graph.facebook.com/v23.0/oauth/access_token
  ?client_id={app-id}
  &client_secret={app-secret}
  &redirect_uri={redirect-uri}
  &code={authorization-code}
```

レスポンス例：
```json
{
  "access_token": "EAAG...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### 4. 長期アクセストークン取得

**Facebook Login の場合：**
```bash
GET https://graph.facebook.com/v23.0/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id={app-id}
  &client_secret={app-secret}
  &fb_exchange_token={short-lived-token}
```

**Instagram Login の場合：**
```bash
POST https://graph.instagram.com/access_token
  ?grant_type=ig_exchange_token
  &client_secret={instagram-app-secret}
  &access_token={short-lived-token}
```

レスポンス例：
```json
{
  "access_token": "IGQVJYdG9...",
  "token_type": "bearer", 
  "expires_in": 5183944
}
```

### トークンリフレッシュ

長期トークンは有効期限前にリフレッシュが必要：

```bash
GET https://graph.facebook.com/v23.0/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id={app-id}
  &client_secret={app-secret}
  &fb_exchange_token={long-lived-token}
```

## トークン検証・管理

### トークン情報の確認
```bash
GET https://graph.facebook.com/v23.0/me?access_token={token}
```

### Instagram User ID 取得
```bash
# Facebook Login の場合
GET https://graph.facebook.com/v23.0/me/accounts?access_token={token}

# レスポンスからInstagram Business Account IDを取得
GET https://graph.facebook.com/v23.0/{page-id}?fields=instagram_business_account&access_token={token}
```

### トークン権限確認
```bash
GET https://graph.facebook.com/v23.0/me/permissions?access_token={token}
```

## エラーハンドリング

### よくある認証エラー

#### 権限不足エラー
```json
{
  "error": {
    "message": "Insufficient permissions for this operation",
    "type": "OAuthException", 
    "code": 10
  }
}
```

**対処法**: 必要な権限をスコープに追加し、ユーザーに再認証を促す

#### トークン期限切れエラー
```json
{
  "error": {
    "message": "Error validating access token: Session has expired",
    "type": "OAuthException",
    "code": 190,
    "error_subcode": 463
  }
}
```

**対処法**: トークンリフレッシュまたは再認証

#### レート制限エラー
```json
{
  "error": {
    "message": "Application request limit reached",
    "type": "OAuthException",
    "code": 4
  }
}
```

**対処法**: リクエスト頻度の調整

## セキュリティベストプラクティス

### 1. トークン保存
```
✅ データベースで暗号化して保存
✅ 環境変数でApp Secret管理
❌ フロントエンドでの長期保存
❌ ログファイルへの出力
```

### 2. HTTPS必須
- 本番環境では必ずHTTPS使用
- リダイレクトURIもHTTPS必須

### 3. State パラメータ
CSRF攻撃防止のため、state パラメータを必ず使用：
```javascript
const state = generateRandomString(32);
// 認証URLにstate を含める
// コールバックで検証
```

### 4. スコープ最小化
必要最小限の権限のみリクエスト

## 実装例（Node.js）

### 環境変数設定
```env
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
INSTAGRAM_APP_ID=your_instagram_app_id  
INSTAGRAM_APP_SECRET=your_instagram_app_secret
REDIRECT_URI=https://yourdomain.com/auth/callback
```

### 認証URL生成
```javascript
const generateAuthURL = (scopes = ['instagram_basic', 'instagram_manage_insights']) => {
  const state = crypto.randomBytes(16).toString('hex');
  const params = new URLSearchParams({
    client_id: process.env.META_APP_ID,
    redirect_uri: process.env.REDIRECT_URI,
    scope: scopes.join(','),
    response_type: 'code',
    state: state
  });
  
  return {
    url: `https://www.facebook.com/v23.0/dialog/oauth?${params}`,
    state: state
  };
};
```

### トークン取得・交換
```javascript
const exchangeCodeForTokens = async (code) => {
  // 短期トークン取得
  const shortTokenResponse = await fetch('https://graph.facebook.com/v23.0/oauth/access_token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: process.env.META_APP_ID,
      client_secret: process.env.META_APP_SECRET,
      redirect_uri: process.env.REDIRECT_URI,
      code: code
    })
  });
  
  const shortToken = await shortTokenResponse.json();
  
  // 長期トークン取得
  const longTokenResponse = await fetch(`https://graph.facebook.com/v23.0/oauth/access_token?grant_type=fb_exchange_token&client_id=${process.env.META_APP_ID}&client_secret=${process.env.META_APP_SECRET}&fb_exchange_token=${shortToken.access_token}`);
  
  const longToken = await longTokenResponse.json();
  
  return {
    accessToken: longToken.access_token,
    expiresIn: longToken.expires_in,
    tokenType: longToken.token_type
  };
};
```

## 運用時の注意点

### 1. トークン監視
- トークン有効期限の監視（30日前にアラート）
- 自動リフレッシュ機能の実装
- 失敗時のフォールバック機能

### 2. ログ管理  
- 認証エラーのログ収集
- 不正アクセス試行の監視
- パフォーマンス指標の追跡

### 3. ユーザー体験
- 権限説明の表示
- エラー時の分かりやすいメッセージ
- 再認証フローの簡素化

これらの仕様に基づいて、PoC段階では最小限の権限（`instagram_basic`, `instagram_manage_insights`）から始めて、段階的に機能を拡張していくことを推奨します。