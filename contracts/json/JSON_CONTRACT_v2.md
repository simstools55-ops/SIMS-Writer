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


## v1.1.1 Canonical output policy
- 入力互換形はRuntimeで正規化し、出力では別名フィールドを混在させない。
- 値がない任意項目に空文字を使用しない。`null`を許容するフィールドはnull、それ以外は省略する。
- 内部リンク評価は adopted / pending / rejected の3状態を保持する。
- confidenceは high / medium / low の3値とし、根拠を説明する。
- LOW_SAMPLE時は標本数とQuery Coverageをwarningまたはinformationへ記録する。
