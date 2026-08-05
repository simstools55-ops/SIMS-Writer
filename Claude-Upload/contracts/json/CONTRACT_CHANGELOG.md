## Contract 2.1 Hotfix - 2026-07-24

- Canonical version field: `contract_version`.
- Canonical changes field: `changes[]` with per-change `implementation_status`.
- Empty strings are forbidden in canonical output.
- Query Coverage uses `coverage_confidence` with `high|medium|low`.
- Legacy aliases remain input-only through Schema Normalizer.

# JSON Contract Changelog

## 2.0

- `preservation_score`を正式化
- `change_budget_percent`へ名称統一
- Rewrite LevelをL0〜L4へ統一
- Rewrite ScopeをS0〜S5へ統一
- `diagnosis`、`risk_level`、`validation`を必須化
- LOW_SAMPLE用`remeasurement_days`を追加
- 未知フィールドを禁止

## 1.x

互換読み取り専用。新規出力には使用しない。
