# GitHub Actions セットアップガイド

Instagram分析アプリの自動データ収集システムのセットアップ手順

## 📋 必要なシークレット設定

GitHub リポジトリの **Settings > Secrets and variables > Actions** で以下を設定:

### Repository Secrets

| Secret名 | 説明 | 取得方法 |
|----------|------|----------|
| `SUPABASE_URL` | Supabaseプロジェクトの URL | Supabaseダッシュボード > Settings > API |
| `SUPABASE_ANON_KEY` | Supabaseの anon キー | Supabaseダッシュボード > Settings > API |
| `INSTAGRAM_APP_ID` | Instagram アプリ ID | Meta for Developers > アプリ設定 |
| `INSTAGRAM_APP_SECRET` | Instagram アプリ シークレット | Meta for Developers > アプリ設定 |

### 設定手順

1. **GitHub リポジトリにアクセス**
   - リポジトリページで **Settings** クリック

2. **Secrets設定ページに移動**
   - 左サイドバーの **"Secrets and variables"** > **"Actions"** クリック

3. **Repository secretsを追加**
   - **"New repository secret"** ボタンをクリック
   - 各シークレットを以下の形式で追加:

#### SUPABASE_URL の設定
```
Name: SUPABASE_URL
Secret: https://your-project-id.supabase.co
```

#### SUPABASE_ANON_KEY の設定
```
Name: SUPABASE_ANON_KEY
Secret: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
⚠️ **注意**: `anon` キー を使用

#### INSTAGRAM_APP_ID の設定
```
Name: INSTAGRAM_APP_ID
Secret: 1234567890123456
```

#### INSTAGRAM_APP_SECRET の設定
```
Name: INSTAGRAM_APP_SECRET
Secret: abcdef1234567890abcdef1234567890
```

## 🚀 ワークフローの実行方法

### 自動実行
- **毎日 JST 09:00** (UTC 00:00) に自動実行
- cron スケジュール: `0 0 * * *`

### 手動実行
1. **Actions タブに移動**
   - リポジトリページで **Actions** クリック

2. **ワークフローを選択**
   - **"Instagram Daily Data Collection"** をクリック

3. **手動実行**
   - **"Run workflow"** ボタンをクリック
   - オプション設定:
     - **Debug mode**: デバッグログを有効化
     - **Test mode**: テスト実行モード (将来の機能)

4. **実行開始**
   - **"Run workflow"** ボタンで実行開始

## 📊 実行結果の確認

### 成功時の確認事項
- ✅ 全ステップが緑色で完了
- 📄 Artifacts に `collection-results-*` ファイルが保存
- 📈 Supabase でデータが更新されている

### 失敗時の対応
- ❌ 赤色で失敗したステップを確認
- 📋 自動的に GitHub Issue が作成される
- 🔍 エラーログを確認してトラブルシューティング

## 🔧 トラブルシューティング

### よくあるエラーと対策

#### 1. 環境変数エラー
```
❌ Missing environment variables: SUPABASE_ANON_KEY
```
**対策**: Repository Secrets の設定を確認

#### 2. Instagram API エラー
```
❌ Instagram API connection failed
```
**対策**: 
- アクセストークンの有効期限を確認
- `/settings/setup` でトークンを更新

#### 3. Supabase 接続エラー
```
❌ Supabase connection failed
```
**対策**:
- SUPABASE_URL と SUPABASE_ANON_KEY を確認
- Supabaseプロジェクトの稼働状況を確認

#### 4. Python 依存関係エラー
```
❌ No module named 'supabase'
```
**対策**: 
- `scripts/requirements.txt` の内容を確認
- Python キャッシュをクリア

### デバッグ方法

#### 1. デバッグモードで実行
- 手動実行時に **Debug mode** を有効化
- 詳細なログが出力される
- 結果ファイルが Artifacts に保存される

#### 2. ログの確認
- 各ステップのログを詳細に確認
- 特に **"Run Instagram data collection"** ステップ

#### 3. Artifacts の確認
- 実行後に生成される以下のファイルを確認:
  - `collection_results_*.json`: 詳細な実行結果
  - `collection_report_*.md`: 人間が読みやすいレポート

## 📈 モニタリング

### 成功率の監視
- Actions タブで過去の実行履歴を確認
- 失敗が続く場合は原因を調査

### データ品質の確認
- Supabase ダッシュボードで実際のデータを確認
- 期待される件数のデータが収集されているかチェック

### アラート対応
- GitHub Issue で失敗通知を受信
- Issue のチェックリストに従って対応

## 🔄 メンテナンス

### 定期メンテナンス項目
- **月1回**: Instagram アクセストークンの有効期限チェック
- **週1回**: 収集データの品質チェック
- **必要時**: Instagram API の制限状況チェック

### アップデート手順
1. コードの変更をリポジトリにプッシュ
2. 手動実行でテスト
3. 問題がなければ自動実行を継続

---

## 📞 サポート

### 問題が解決しない場合
1. GitHub Issue を確認
2. 上記のトラブルシューティングを実施
3. 必要に応じて手動でデータ収集を実行

### 緊急時の対応
- Instagram API の制限に達した場合: 翌日まで待機
- Supabase がダウンした場合: Supabase の Status ページを確認
- 長期間の障害: 手動でのデータ収集スクリプト実行を検討