# SIMS Feedback JSON Contract v2.0

The default machine contract for Quality Freeze is `SIMS_FEEDBACK_V1` version `2.0`.

## Frozen rules

- The schema is closed: contract-external fields are prohibited.
- `diagnosis` is an array because `LOW_SAMPLE` may coexist with an opportunity diagnosis.
- Rewrite levels are L0–L4 only. Legacy L5 is invalid.
- `change_budget_percent` is the canonical field name.
- `changes` contains only implemented changes and requires `expected_effect`.
- `change_flags` and `new_values` must match the human-facing output.
- `validation.estimated_change_percent` must not exceed `change_budget_percent`.
- `validation.status=FAIL` requires `decision=REVIEW_REQUIRED` or `BLOCK`.
- `LOW_SAMPLE` normally prevents `confidence=high`.
- A changed SEO title normally requires `next_action=remeasure` unless manual review is required.

The authoritative schema is `schemas/SIMS_FEEDBACK_V1.schema.json`.
