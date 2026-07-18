# Quality Report Specification v1.0

## 目的
各フェーズの判定根拠を内部監査用に集約する。利用者向け本文には表示しない。

## 必須要素
- phase status
- score（存在する場合）
- issue count
- blocking count
- warning count
- confidence
- risk
- final decision
- rule trace

## Status正規化
- PASS
- PASS_WITH_SUGGESTIONS
- REVIEW
- FAIL
- NOT_EVALUATED

## 用途
- 回帰テスト
- 不具合調査
- Prompt/Knowledge改善
- 誤判定原因分析
- バージョン比較
- Runtime Health集計

## 禁止事項
- 内部推論文の保存
- 記事本文への混入
- 元記事全文の不要な複製
