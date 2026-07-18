# SIMS Feedback JSON Contract v2.0

## 契約名

`SIMS_FEEDBACK_V2`

## 目的

SIMS Writerの診断、改善方針、変更範囲、保護状態、Validation結果をSIMS-Blog-Manager等へ安全に返す。

## 必須フィールド

- `contract_version`
- `article_id`
- `url`
- `status`
- `diagnosis`
- `primary_intent`
- `preservation_score`
- `change_budget_percent`
- `rewrite_level`
- `rewrite_scope`
- `risk_level`
- `changed_sections`
- `protected_elements`
- `validation`
- `recommendation_reason`

## 列挙値

- status: `PASS`, `PASS_WITH_WARNING`, `IMPROVEMENT_REQUIRED`, `NO_CHANGE`, `FAIL`
- diagnosis: `POSITION_OPPORTUNITY`, `LOW_SAMPLE`, `CTR_OPPORTUNITY`, `CONTENT_GAP`, `INTENT_MISMATCH`, `STABLE`, `UNKNOWN`
- rewrite_level: `L0`, `L1`, `L2`, `L3`, `L4`
- rewrite_scope: `S0`, `S1`, `S2`, `S3`, `S4`, `S5`
- risk_level: `LOW`, `MEDIUM`, `HIGH`
- validation.result: `PASS`, `PASS_WITH_WARNING`, `FAIL`, `UNVERIFIABLE`

## 互換性

V1入力は読み取り可能だが、v0.2.0以降の出力はV2を標準とする。
未知フィールドは原則拒否し、SchemaをSingle Source of Truthとする。
