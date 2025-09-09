# 07. Facebook/Instagram Graph API - 権限リファレンス

**最終更新**: 2025年01月09日  
**情報源**: Meta for Developers 公式ドキュメント  
**参照URL**: 
- [Facebook Permissions Reference](https://developers.facebook.com/docs/permissions/reference)
- [Instagram Platform Overview](https://developers.facebook.com/docs/instagram-platform)

## 2025年権限システム概要

### アクセスレベル
- **Standard Access**: 基本的な権限（App Review不要）
- **Advanced Access**: 詳細なデータアクセス（App Review必要）

### 対象アカウント制限
- ✅ Instagram Professional Account（Business/Creator）のみ
- ❌ Consumer（個人）アカウントは利用不可

---

## 権限詳細リスト

### Instagram関連権限

#### 🔴 `instagram_basic` - Instagram基本アクセス
- **説明**: Instagram Business Accountの基本プロフィール・メディア情報取得
- **用途**: ユーザー名、ID、基本メタデータ
- **レビュー**: Standard Access（App Review不要）
- **依存権限**: `pages_read_user_content`, `pages_show_list`
- **取得可能データ**:
  - プロフィール情報（username, media_count）
  - メディア一覧（投稿日、タイプ、いいね数、コメント数）
  - 基本的なメディアメタデータ

#### 🔴 `instagram_manage_insights` - インサイト管理権限
- **説明**: Facebook連携Instagram Business Accountのインサイトデータアクセス
- **用途**: メタデータ、データインサイト、ストーリーインサイト取得
- **レビュー**: **Advanced Access（App Review必要）**
- **依存権限**: `instagram_basic`, `pages_read_engagement`, `pages_show_list`
- **取得可能データ**:
  - リーチ、インプレッション
  - エンゲージメント率
  - 保存数、シェア数
  - 動画視聴数・視聴率
  - フォロワーインサイト（人口統計）

---

### Pages関連権限

#### 🔴 `pages_show_list` - ページ一覧表示
- **説明**: ユーザーが管理するページの一覧取得
- **用途**: ページ管理確認、Instagram Business Account ID特定
- **レビュー**: Standard Access（App Review不要）
- **依存権限**: なし
- **取得可能データ**:
  - 管理ページ一覧
  - ページに連携されたInstagram Business Account情報

#### 🔴 `pages_read_engagement` - ページエンゲージメント読み取り
- **説明**: ページ上のコンテンツとエンゲージメントデータ読み取り
- **用途**: フォロワーデータ（名前、PSID）、プロフィール写真
- **レビュー**: **Advanced Access（App Review必要）**
- **依存権限**: `pages_show_list`
- **取得可能データ**:
  - 投稿、写真、動画、イベント
  - フォロワー詳細データ

#### 🟡 `pages_read_user_content` - ページユーザーコンテンツ読み取り
- **説明**: ページ上のユーザー作成コンテンツ読み取り
- **用途**: ユーザーまたは他のページの投稿、コメント、評価
- **レビュー**: **Advanced Access（App Review必要）**
- **依存権限**: `pages_show_list`
- **取得可能データ**:
  - ユーザー投稿、コメント
  - ページ評価・レビュー

#### 🟡 `business_management` - ビジネス管理
- **説明**: Business Manager API経由での読み書きアクセス
- **用途**: 広告アカウントなどのビジネス資産管理
- **レビュー**: **Advanced Access（App Review必要）**
- **依存権限**: `pages_read_engagement`, `pages_show_list`
- **取得可能データ**:
  - ビジネス資産（広告アカウント等）
  - アカウント権限管理

---

## 今回のプロジェクトでの権限要件

### 🔴 必須権限（即座に必要）
| 権限 | 現在の状況 | 用途 | レビュー要否 |
|------|-----------|------|-------------|
| `instagram_basic` | ✅ 取得済み | メディア一覧、基本情報 | ❌ Standard |
| `instagram_manage_insights` | ❌ **不足** | **リーチ、インプレッション** | ✅ **Advanced** |
| `pages_show_list` | ✅ 取得済み | IG Business Account ID | ❌ Standard |
| `pages_read_engagement` | ❌ **不足** | 詳細エンゲージメント | ✅ **Advanced** |

### 🟡 推奨権限（将来的に有用）
| 権限 | 現在の状況 | 用途 | レビュー要否 |
|------|-----------|------|-------------|
| `pages_read_user_content` | ❌ 不足 | ユーザーコメント詳細 | ✅ Advanced |
| `business_management` | ❌ 不足 | ビジネス資産管理 | ✅ Advanced |

---

## 投稿分析ページでのデータマッピング

### ✅ 現在取得可能（Standard Access）
- 投稿日、サムネイル
- メディアタイプ（画像/動画/カルーセル）
- いいね数、コメント数
- ユーザー名、フォロワー数

### ❌ 取得不可（Advanced Access必要）
- **リーチ数** → `instagram_manage_insights`
- **インプレッション数** → `instagram_manage_insights`
- **保存数、シェア数** → `instagram_manage_insights`
- **視聴数、視聴率** → `instagram_manage_insights`
- **エンゲージメント率** → `instagram_manage_insights`

---

## App Reviewプロセス

### Advanced Access取得手順
1. **アプリケーション準備**: 
   - 実装完了
   - テスト環境準備
   - ユースケース文書作成

2. **Review申請**: 
   - 各権限の使用目的説明
   - スクリーンキャスト動画提出
   - プライバシーポリシー提出

3. **審査期間**: 通常2-7営業日

4. **承認後**: Advanced Access権限が有効化

### Review要求項目
- **ビジネス検証**: Facebook Business Managerアカウント
- **アプリ目的の明確化**: Instagram分析ダッシュボード
- **ユーザーメリット**: ビジネス成果向上支援
- **データ使用方針**: プライバシー保護の実装

---

## 開発フェーズでの権限戦略

### Phase 1: PoC開発（現在）
```
✅ Standard Access権限のみ使用
- instagram_basic
- pages_show_list
- 基本的な投稿データで機能確認
```

### Phase 2: 完全版開発
```
✅ Advanced Access申請・取得
- instagram_manage_insights
- pages_read_engagement
- 全機能実装
```

### Phase 3: 本番運用
```
✅ Advanced Access運用
- 全メトリクス取得
- リアルタイム分析提供
```

---

## 権限エラー対応

### よくある権限エラー
```json
{
  "error": {
    "message": "Insufficient permissions for this operation",
    "type": "OAuthException",
    "code": 10
  }
}
```

### 対処法
1. **権限確認**: `/me/permissions` エンドポイントで現在の権限確認
2. **依存関係確認**: 必要な依存権限が全て付与されているか確認
3. **App Review状況確認**: Advanced Access権限の審査状況確認
4. **再認証**: 新しい権限でユーザーに再認証を促す

---

## まとめ

**即座に必要な対応:**
1. ✅ `instagram_manage_insights` のApp Review申請
2. ✅ `pages_read_engagement` のApp Review申請
3. 📝 App Review用ドキュメント準備
4. 🎥 アプリケーションデモ動画作成

**現在の状況:**
- Basic機能は実装可能（Standard Access）
- Advanced機能にはApp Review必須（Advanced Access）
- Review期間: 2-7営業日