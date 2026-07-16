# Model Adapter Architecture v1.0

Model Adapterは、SIMS Writer Runtime Coreと外部生成モデルの境界である。
正式なKnowledge、Decision、Pattern、Quality Ruleを独自に保持せず、Runtime ViewとOutput Schemaを各Provider形式へ変換する。

## 共通処理

1. Context Bundleを構築する
2. Provider Requestを生成する
3. Transportを通じて応答を取得する
4. JSON Outputを抽出する
5. Content Draft Contract相当の必須項目を検証する
6. Provider固有情報をGeneration Recordへ分離する

## 対応Adapter

- Claude Messages互換Adapter
- OpenAI Responses互換Adapter
- Generic Chat JSON Adapter
- Fixture Adapter（自動テスト専用）

本PackageはAdapter構造と検証済みローカル実装を提供する。外部APIの認証情報やライブ呼び出し結果は同梱しない。
