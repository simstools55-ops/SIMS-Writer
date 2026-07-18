# Validation Layer v0.2.0

## Status values

- `PASS`
- `PASS_WITH_WARNING`
- `FAIL`

## Blocking checks

| Code | Check | Failure condition |
|---|---|---|
| VAL-CONTRACT-001 | JSON contract | Schema, required keys, types, enum, or strict field order is violated |
| VAL-INTENT-001 | Primary intent | Proposed title/intro/headings/conclusion change the primary intent |
| VAL-PRESERVE-001 | Protected elements | Protected element is removed, altered, or replaced without approval |
| VAL-BUDGET-001 | Change budget | Estimated change exceeds `change_budget_percent` |
| VAL-SCOPE-001 | Rewrite declaration | Actual change does not match Rewrite Level or Scope |
| VAL-FLAG-001 | Change flags | Machine flags/new values differ from human output |
| VAL-FACT-001 | Unsupported claim | Material numeric, time-sensitive, or performance claim lacks basis |
| VAL-LANG-001 | Output language | English analysis or internal reasoning appears in user output |

## Warning checks

| Code | Check | Warning condition |
|---|---|---|
| VAL-SAMPLE-001 | Sample size | `LOW_SAMPLE` applies; recommendation must be conservative |
| VAL-TITLE-001 | Title length | Recommended >40 and <=45 characters |
| VAL-META-001 | Meta length | Recommended >120 and <=140 characters |
| VAL-FAQ-001 | FAQ necessity | FAQ adds little new value or duplicates body wording |
| VAL-EVIDENCE-001 | Evidence availability | Non-blocking source or candidate could not be verified |

## Automatic repairs

- Length overflow: shorten only the overflowing component.
- Flag mismatch: correct flags/new values to match the actual output.
- FAQ duplication: remove or merge the duplicate FAQ.
- Budget overflow: revert the lowest-priority changes until within budget.
- Intent mismatch: restore the original primary intent and regenerate only affected components.

## Validation result object

```json
{
  "status": "PASS",
  "checks": [
    {"code": "VAL-INTENT-001", "status": "PASS", "message": ""}
  ],
  "estimated_change_percent": 18,
  "notes": []
}
```

A `FAIL` result cannot be presented as publish-ready. A warning lowers confidence when it materially affects the decision.
