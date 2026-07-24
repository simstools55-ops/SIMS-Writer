# SIMS Writer Contract Validation 2.1

最終出力は`SIMS_FEEDBACK_V2` / `contract_version: 2.1`に固定する。

## Blocking rules

- VAL-CONTRACT-001: Canonical Schemaに適合しない。
- VAL-CONTRACT-002: `version`、`diagnosis_code`、`change_flags`などLegacy fieldが最終出力に残る。
- VAL-CONTRACT-003: 空文字または不正なnullが残る。
- VAL-CONTRACT-004: `changes[]`または全体の`implementation_status`が欠落・不正。
- VAL-CONTRACT-005: Query Coverageが`coverage_confidence`と4分類を持たない。

Normalizerは旧形式を入力互換として受け入れるが、最終出力を修復できない場合はFAILとする。
