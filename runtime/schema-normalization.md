# Schema Normalization — Contract 2.1 Hotfix

旧2.0入力の`version`、`diagnosis_code`、`change_flags`、空文字、旧Validation、旧Query Coverageを受け入れる。最終出力は必ず`contract_version: 2.1`、`diagnosis`、`changes[]`、`implementation_status`、`coverage_confidence`へ正規化し、Legacy fieldを残さない。

空文字は、任意フィールドなら省略し、明示的な未設定を許容するフィールドだけnullとする。
