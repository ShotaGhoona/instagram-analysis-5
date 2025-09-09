# Instagram API Verification

## セットアップ手順

### 1. 仮想環境の有効化
```bash
cd verification
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows
```

### 2. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定
```bash
cp .env.example .env
```

`.env`ファイルに以下の情報を設定：
- `INSTAGRAM_APP_ID`: アプリID
- `INSTAGRAM_APP_SECRET`: アプリシークレット
- `INSTAGRAM_ACCESS_TOKEN`: アクセストークン
- `INSTAGRAM_BUSINESS_ACCOUNT_ID`: ビジネスアカウントID（Graph API用）

### 4. スクリプト実行
```bash
python scripts/01-basic-user-info.py
```

## ディレクトリ構造
```
verification/
├── venv/                       # Python仮想環境
├── requirements.txt            # 依存パッケージ
├── .env.example               # 環境変数テンプレート
├── .env                       # 実際の環境変数（gitignore対象）
├── utils/                     # 共通処理モジュール
│   ├── api_client.py
│   └── data_formatter.py
├── api-references/            # API仕様書
│   ├── 01-instagram-platform.md
│   ├── 02-overview.md
│   ├── 03-media-api.md
│   ├── 04-insights-metrics-api.md
│   ├── 05-authentication-tokens.md
│   └── 06-endpoints-list.md
└── endpoint-tests/            # エンドポイント別検証
    ├── 01-me/
    │   ├── 01-basic-user-info.py
    │   ├── 01-output-data.json
    │   └── 01-report.md
    ├── 02-accounts/
    │   ├── 01-page-list.py
    │   ├── 01-output-data.json
    │   └── 01-report.md
    ├── 03-media-list/
    │   ├── 01-media-retrieval.py
    │   ├── 01-output-data.json
    │   └── 01-report.md
    └── 04-media-insights/
        ├── 01-insights-metrics.py
        ├── 01-output-data.json
        └── 01-report.md
```

## 検証フロー
1. **エンドポイント別検証**: 各フォルダで個別に実施
2. **1エンドポイント = スクリプト = アウトプット = レポート**
3. **段階的検証**: 認証 → 基本データ取得 → インサイト取得の順序

## スクリプト作成ルール

### 1. ログ出力規則
- **ログは日本語で記述する**
- **アイコンを活用してわかりやすく表示**
  - ✅ 成功
  - ❌ エラー
  - ⚠️ 警告
  - 🔍 情報
  - 📊 データ
  - 🚀 開始
  - 🏁 完了

### 2. 出力形式
```python
print("🚀 Instagram Graph API検証を開始します...")
print("✅ 成功: ユーザー情報を取得しました")
print("❌ エラー: 認証に失敗しました")
print("⚠️ 警告: Instagram Business Accountが見つかりません")
print("🔍 情報: 5件のメディアを取得中...")
print("📊 データ: リーチ数 1,234, インプレッション数 2,345")
```

### 3. エラーハンドリング
- すべての例外をキャッチして日本語で出力
- エラー詳細をJSONファイルに記録
- ユーザーフレンドリーなエラーメッセージを表示

### 4. 実行結果保存
- `01-output-data.json`: 構造化されたデータ
- `01-report.md`: 人間が読みやすいレポート（実行後自動更新）
- 日本語コメント付きのJSON出力

---

## ⚠️ 重要: Instagram API 最新情報（2025年）

### Instagram Basic Display API - 廃止済み
- **2024年12月4日に完全廃止**
- 個人アカウント向けAPI接続は終了
- 新規開発では使用不可

### Instagram Graph API - 現在の標準
- **Graph API v22.0（2025年最新版）を使用**
- **プロフェッショナルアカウント（Business/Creator）のみ対応**
- 個人アカウントは使用不可

### 2025年の重要な変更点

#### 1. アカウント要件
- ✅ **ビジネスアカウント または クリエイターアカウント必須**
- ❌ 個人アカウント利用不可
- ✅ Facebookページとのリンクが必要

#### 2. API移行期限
- **2025年4月21日**: レガシーエンドポイント完全廃止
- 新しいIG User, IG Media, IG Comment オブジェクトへの移行必須

#### 3. 新機能
- **Viewsメトリクス**: 全メディアタイプ（Reels、Live、Photos、Carousels、Stories）
- 統一されたIG オブジェクト（IG User、IG Media、IG Comment）

### API エンドポイント
- **Base URL**: `https://graph.facebook.com/v22.0/`
- **メディア取得**: `https://graph.instagram.com/me/media`
- **公式ドキュメント**: [Meta for Developers - Instagram Platform](https://developers.facebook.com/docs/instagram-platform/)

### 検証での注意事項
1. **Professional アカウントでのテスト必須**
2. **Graph API v22.0 エンドポイントを使用**
3. **Basic Display API コードは参考程度**
4. **App Review プロセスが本番環境で必要**