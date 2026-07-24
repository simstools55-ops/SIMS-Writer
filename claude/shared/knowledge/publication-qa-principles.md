# Publication QA Principles

## Purpose

改善案を公開前に独立評価し、局所的かつ安全に修正できる欠陥は修正後に再評価する。

## Common Principles

- 記事品質と機械連携Contract品質を分離して評価する。
- 公開判定は `PASS / PASS_WITH_WARNING / PASS_WITH_MINOR_FIX / PASS_WITH_REQUIRED_FIX / FAIL` を用いる。
- 自動修正は、正解が入力情報から一意に決まる局所欠陥に限定する。
- Primary Intent、主要結論、体験談、独自評価、Winner QueryをQAが独断で変更しない。
- 数値、本文とFAQ、内部リンク状態、Contract、Validationの相互整合を確認する。
- 修正後は必ず同じ評価を再実行する。
- 重大な不整合や検証不能な高リスク主張が残る場合は公開を停止する。
