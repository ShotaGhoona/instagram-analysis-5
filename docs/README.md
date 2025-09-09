# Instagram Analytics App - 開発指南書

Instagram分析アプリ（PoC）の開発を体系的に進めるための指南書です。

## 📋 開発フロー

### 1. 要件確認フェーズ
```bash
# 関連する要件定義ファイルを全て読む
docs/requirement-definition/01-requirement-summary.md      # 全体概要
docs/requirement-definition/02-database-schema.md         # DB設計
docs/requirement-definition/03-page-design.md            # UI設計
docs/requirement-definition/11-backend-architecture.md    # バックエンド設計
docs/requirement-definition/12-frontend-architecture.md   # フロントエンド設計
```

### 2. タスク選定フェーズ
```bash
# 完了チェックリストで次のタスクを確認
docs/requirement-definition/21-completion-checklist.md

# 優先度順でタスク選択
# 🔥 高優先度 → 🟡 中優先度 → 🟢 低優先度
# 未完了（❌）→ 進行中（🔄）→ 完了（✅）
```

### 3. 戦略立案フェーズ
```bash
# 実装戦略書を作成
docs/implementation-strategy/{TaskID}.md

# 戦略書テンプレート:
# - 概要: 簡潔な説明
# - 現状確認: 既存実装・依存関係確認
# - 実装戦略: ステップ別手順（時間見積もり付き）
# - ファイル構成: 作成・修正するファイル一覧
# - 完了条件: チェックリスト形式
# - PoC配慮: 制約・簡略化項目
```

### 4. 実装フェーズ
```bash
# TodoWrite で進捗管理
# 戦略書の手順に従って段階的実装
# 各ステップ完了時にTodo更新（pending → in_progress → completed）
```

### 5. 完了報告フェーズ
```bash
# 実装完了報告書を作成
docs/implementation-strategy/{TaskID}-report.md

# 報告書テンプレート:
# - 実施結果: ✅/❌、実施時間、状況
# - 主な成果: 箇条書きで簡潔に
# - 課題・備考: 問題があった場合
# - 次のタスク: 次に進むべきタスク

# チェックリスト更新
docs/requirement-definition/21-completion-checklist.md
# ❌ 未完了 → ✅ 完了
```

## 🎯 実装例: F0701-F0702 (アカウント選択UI + 切り替えロジック)

### 1. 要件確認
```bash
# 読んだファイル:
- 12-frontend-architecture.md  # Context設計確認
- 03-page-design.md           # UI仕様確認
- 21-completion-checklist.md  # タスク詳細確認
```

### 2. タスク選定
```bash
# 選択したタスク:
☐ F0701: アカウント選択UIの実装
☐ F0702: アカウント切り替えロジックの実装

# 理由: B0202（アカウント情報取得API）完了後の論理的な次ステップ
```

### 3. 戦略立案
```bash
# 作成したファイル:
docs/implementation-strategy/F0701-F0702.md

# 戦略内容:
1. APIクライアント関数追加 (15分)
2. アカウントContext作成 (45分)
3. Root Layout更新 (10分)
4. アカウント選択Combobox作成 (40分)
5. Header統合 (20分)
合計: 約2時間
```

### 4. 実装
```bash
# 実装したファイル:
- contexts/account-context.tsx       # 新規作成
- components/account/account-selector.tsx  # 新規作成
- lib/api.ts                        # 型定義追加
- components/providers.tsx           # Provider統合
- components/layout/header.tsx       # 統合

# TodoWrite による進捗管理:
✅ APIクライアント関数追加
✅ アカウントContext作成  
✅ Root Layout更新
✅ アカウント選択Combobox作成
✅ Header統合
```

### 5. 完了報告
```bash
# 作成したファイル:
docs/implementation-strategy/F0701-F0702-report.md

# チェックリスト更新:
| F0701 | アカウント選択UI | ❌ 未完了 | → | ✅ 完了 |
| F0702 | 切り替えロジック | ❌ 未完了 | → | ✅ 完了 |
```

## 📚 ファイル構成

```
docs/
├── README.md                     # この指南書
├── requirement-definition/       # 要件定義
│   ├── 01-requirement-summary.md
│   ├── 02-database-schema.md
│   ├── 03-page-design.md
│   ├── 11-backend-architecture.md
│   ├── 12-frontend-architecture.md
│   └── 21-completion-checklist.md
└── implementation-strategy/       # 実装戦略・報告
    ├── README.md                 # 実装ルール
    ├── {TaskID}.md              # 戦略書
    └── {TaskID}-report.md       # 完了報告書
```

## ⚡ 効率化のコツ

### 戦略書作成
- **2-3分で読める分量** に抑える
- **時間見積もり** を必ず含める
- **依存関係** を明確にする
- **PoC制約** を忘れずに記載

### 実装作業
- **TodoWrite** でタスクを細分化
- **段階的完了** でモチベーション維持
- **エラー時は戦略書を更新** して記録

### 完了報告
- **2秒でキャッチアップ可能** な簡潔さ
- **次のタスク** を明確に提示
- **チェックリスト更新** を忘れずに

## 🎖️ 品質基準

- **動作すればOK** - 完璧を求めない
- **PoC要件遵守** - スコープ拡大禁止
- **将来の拡張性より現在の動作** を優先
- **エラーハンドリングは最小限**

---

この指南書に従って、体系的かつ効率的にInstagram Analytics Appの開発を進めましょう！