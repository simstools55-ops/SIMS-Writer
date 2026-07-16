# CTR Improvement Vertical Slice v1.0

## Scope

- SBM JSON入力
- CTR改善対象の正規化
- SEOタイトル、導入、FAQの変更要否Decision
- 必要Patternのみ選択
- 構造化Draft生成
- 42 Quality Rule / 7 Gate実行
- Targeted Refinement
- Publication Package生成

## Non-goals

- 競合検索のライブ取得
- URL本文の自動取得
- 外部LLM APIのライブ実行
- CTR上昇の保証

## Decision

タイトルのクエリ整合、表示回数、CTR、平均順位を用いる。入力データが不足する場合は、断定的な性能判断を避け、検索意図整合を優先する。
