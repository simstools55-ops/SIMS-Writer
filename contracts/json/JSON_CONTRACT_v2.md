# SIMS Feedback JSON Contract v2.0

## 契約名

`SIMS_FEEDBACK_V2`

## 方針

V1で利用していた `changes`、`new_values`、`expected_effect`、`next_action` を維持しながら、診断・保護・変更量・Validationを構造化する。SBMが段階的に移行できる加算型の契約とする。

## 主な追加項目

- `diagnosis`: 複数診断を配列で保持
- `primary_intent` / `secondary_intent`
- `preservation_score` / `protected_elements`
- `change_budget_percent`
- `rewrite_level` / `rewrite_scope` / `risk`
- `effect_confidence`: 改善案への自信と効果予測への自信を分離
- `validation`: タイトル長、意図整合、変更量、保護対象を記録
- `internal_link_evaluation`: 追加・保留・不採用件数（任意）

## 診断

`POSITION_OPPORTUNITY`, `LOW_SAMPLE`, `CTR_OPPORTUNITY`, `CONTENT_GAP`, `INTENT_MISMATCH`, `STRONG_CURRENT_PERFORMANCE`, `STABLE`, `INPUT_INCOMPLETE`, `UNKNOWN`, `OTHER`

`LOW_SAMPLE`は他診断と併記できる。例：`["POSITION_OPPORTUNITY", "LOW_SAMPLE"]`。

## 互換性

- V1入力は読み取り可能とする。
- 新規出力はV2を標準とする。
- V1しか受け取れない連携先が明示された場合に限りV1へフォールバックする。
- SchemaをSingle Source of Truthとする。
