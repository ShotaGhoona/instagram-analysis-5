# 05-media-insights - 投稿別インサイト検証

## 概要

投稿分析ページに必要な投稿別インサイトメトリクスの取得を検証します。

**検証エンドポイント:**
```
GET /{ig-media-id}/insights?metric=reach
GET /{ig-media-id}/insights?metric=views      # 動画視聴数（統一メトリクス）
GET /{ig-media-id}/insights?metric=video_views # 廃止（2025年4月）
```

## 検証スクリプト

### 01-media-insights.py 🔑
投稿別インサイトの取得テスト（長期トークン対応済み）

**検証項目:**
- リーチ数 (`metric=reach`) - 全投稿タイプ対象
- シェア数 (`metric=shares`) - 全投稿タイプ対象
- 保存数 (`metric=saved`) - 全投稿タイプ対象
- 動画視聴数 (`metric=video_views`) - VIDEO投稿のみ対象（廃止メトリクス）
- メディアタイプ別の対応確認
- インサイトデータの取得可用性

### 02-video-insights.py 🔑
VIDEO投稿の拡張検索と動画視聴数検証（長期トークン対応済み）

**検証項目:**
- VIDEO投稿の拡張検索（最大10ページ）
- 動画視聴数 (`metric=video_views`) - 廃止メトリクスの詳細検証
- リーチとの比較分析

### 03-views-metric.py 🎉
**新統一メトリクス検証（完全成功）**

**検証項目:**
- 統一視聴数 (`metric=views`) - **現在の正式メトリクス**
- 廃止メトリクス (`metric=video_views`) - 廃止確認
- リーチ (`metric=reach`) - 比較検証
- Views/Reach比率分析

**実行方法:**
```bash
cd verification
python endpoint-tests/05-media-insights/01-media-insights.py  # 基本検証
python endpoint-tests/05-media-insights/02-video-insights.py  # VIDEO検索
python endpoint-tests/05-media-insights/03-views-metric.py    # 新メトリクス（推奨）
```

**前提条件:**
- `01-me/01-output-data.json` が存在すること
- `02-refresh_access_token/01-output-data.json` が存在すること（長期トークン）
- Instagram Business Accountに投稿データが存在すること

## 🎉 検証結果サマリー

### ✅ 完全成功項目
- **統一視聴数メトリクス (`views`)**: 100%成功 - **投稿分析ページ実装可能**
- **リーチメトリクス (`reach`)**: 100%成功
- **長期トークン**: 全スクリプト対応完了

### ❌ 廃止確認項目  
- **動画視聴数メトリクス (`video_views`)**: 2025年4月廃止（予想通り0%成功）

### 期待する結果

#### リーチメトリクス
- IMAGE投稿: リーチ数取得成功
- CAROUSEL_ALBUM投稿: リーチ数取得成功  
- VIDEO投稿: リーチ数取得成功

#### シェア・保存メトリクス
- IMAGE投稿: シェア数・保存数取得テスト
- CAROUSEL_ALBUM投稿: シェア数・保存数取得テスト
- VIDEO投稿: シェア数・保存数取得テスト

#### 動画視聴数メトリクス（統一版）
- VIDEO投稿: **統一視聴数 (`views`) 取得成功** 🎉 (03-views-metric.pyで検証済み)
- IMAGE/CAROUSEL投稿: 統一視聴数 (`views`) 取得成功 (03-views-metric.pyで検証済み)
- 旧メトリクス (`video_views`): 廃止のため取得失敗（正常）

## 📊 投稿分析ページ対応状況

**完全対応可能項目:**
- ✅ 投稿日・サムネイル・タイプ: 取得済み
- ✅ リーチ: 全投稿タイプで取得成功
- ✅ いいね・コメント: 取得済み
- ✅ **視聴数: 統一メトリクスで取得成功**
- 🔶 **シェア数: テスト実行中**
- 🔶 **保存数: テスト実行中**
- ✅ エンゲージメント率: 計算可能

## 出力ファイル

- `01-output-data.json` - 基本インサイト検証結果
- `02-output-data.json` - VIDEO投稿検索結果
- `03-output-data.json` - 統一メトリクス検証結果（**推奨データ**）
- `03-report.md` - 完全成功レポート