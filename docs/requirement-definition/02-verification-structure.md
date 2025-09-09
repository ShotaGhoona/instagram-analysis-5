# 検証フェーズ フォルダ構造設計

## 目的
Meta API（Instagram）から取得可能なデータを段階的に検証し、各スクリプトの結果を体系的に記録・管理する。

## フォルダ構造

```
verification/
├── venv/                       # Python仮想環境
├── requirements.txt            # 依存パッケージ
├── .env.example               # 環境変数テンプレート
├── .env                       # 実際の環境変数（gitignore対象）
├── scripts/                   # 検証スクリプト
│   ├── 01-basic-user-info.py
│   ├── 02-media-list.py
│   ├── 03-media-details.py
│   ├── 04-account-insights.py
│   ├── 05-media-insights.py
│   └── ...
├── outputs/                   # スクリプトの出力結果
│   ├── 01-basic-user-info.json
│   ├── 02-media-list.json
│   ├── 03-media-details.json
│   ├── 04-account-insights.json
│   ├── 05-media-insights.json
│   └── ...
├── reports/                   # 検証レポート
│   ├── 01-basic-user-info.md
│   ├── 02-media-list.md
│   ├── 03-media-details.md
│   ├── 04-account-insights.md
│   ├── 05-media-insights.md
│   └── ...
├── utils/                     # 共通処理
│   ├── api_client.py
│   └── data_formatter.py
└── README.md                  # 検証手順・環境構築方法
```

## 設計原則

### 1スクリプト = 1アウトプット = 1レポート
- `scripts/XX-feature-name.py` → `outputs/XX-feature-name.json` → `reports/XX-feature-name.md`
- 番号順での実行により段階的検証が可能
- 過去の検証履歴を完全保持

### PoC適合設計
- 複雑すぎない構造でスピード重視
- 必要十分な情報管理
- 後のAPI設計フェーズへの連携を考慮

## 次のアクション
1. App Secret・短期トークンの取得（手動）
2. 検証環境のセットアップ
3. 01-basic-user-info.pyからの段階的検証開始