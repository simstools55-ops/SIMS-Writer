# Stage 9: Quality Validation

## 目的
Quality RuleとGateでDraftを評価する。

## 状態
`pending / running / passed / passed_with_warning / failed / blocked / skipped / manual_review_required`

## 原則
入力と出力はContractで検証し、失敗を正常完了として扱いません。


## v3.0.1
Classify findings into SEO Critical and Quality Recommendation. Only unresolved SEO Critical findings enter the repair loop or block publication.
