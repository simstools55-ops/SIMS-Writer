# Stage 2: Normalization

## 目的
外部入力をWriting Requestへ正規化する。

## 状態
`pending / running / passed / passed_with_warning / failed / blocked / skipped / manual_review_required`

## 原則
入力と出力はContractで検証し、失敗を正常完了として扱いません。
