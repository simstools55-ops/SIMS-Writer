# Contract Regression Test Manifest

Version: 1.0.0  
Target contract: `SIMS_FEEDBACK_V1` version `1.2`

## 1. Purpose

This manifest defines regression tests for Phase A1 Contract Validation.

The first baseline consists of the nine recovered JSON outputs from the previous article test.

## 2. Baseline fixtures

| Fixture | Article ID | Primary validation focus |
|---|---|---|
| A000001.txt | A000001 | introduction/body boundary, change flags |
| A000001-A4.txt | A000001 | duplicate ArticleID with different URL, self-link warning |
| A000004.txt | A000004 | standard structure and enum validation |
| A000006.txt | A000006 | graceful degradation with high confidence |
| A000008.txt | A000008 | warning and confidence relationship |
| A000020.txt | A000020 | preserved body and internal links |
| A000036.txt | A000036 | high-confidence clean case |
| A000135.txt | A000135 | estimated main query and estimated_fields |
| A000369.txt | A000369 | internal link true with body false |

The missing tenth fixture may be added later without blocking Phase A1 implementation.

## 3. Baseline findings to preserve as tests

### T-A1-001 JSON parse

Expected:

- All baseline files parse successfully.

### T-A1-002 External version

Expected:

- `format` equals `SIMS_FEEDBACK_V1`.
- `version` equals `1.2`.

### T-A1-003 Required fields

Expected:

- Every required top-level field exists.

### T-A1-004 Changes shape

Expected:

- All nine approved keys exist.
- All values are boolean.
- No unknown change key exists.

### T-A1-005 Information type normalization

Input condition:

- Some historical outputs use a string.

Expected after adapter normalization:

- `information` is always an array of strings.

### T-A1-006 Warning compatibility

Expected:

- `warnings` remains an array of strings.
- Every non-empty warning begins with a registered warning code followed by `: `.

### T-A1-007 Duplicate ArticleID detection

Input:

- `A000001.txt`
- `A000001-A4.txt`

Expected:

- The system detects the same ArticleID associated with different URLs.
- `WC_ARTICLE_ID_URL_MISMATCH` is raised as blocking.
- The conflicting output is not registered.

### T-A1-008 Main query source enum

Allowed values:

- `manual`
- `search_console`
- `estimated`

Expected:

- No other value passes.

### T-A1-009 Estimated main query

Expected:

- `main_query_source: estimated` requires `estimated_fields` to contain `main_query`.
- Other sources must not mark `main_query` as estimated.

### T-A1-010 Execution mode enum

Allowed values:

- `standard`
- `graceful_degradation`

Expected:

- Graceful degradation includes a missing-input explanation in `information`.

### T-A1-011 Introduction/body boundary

Expected:

- A change before the first H2 sets `introduction: true`.
- It does not set `body: true` unless text under an H2 changes.

### T-A1-012 Internal-link flag

Expected:

- Candidate review alone keeps `internal_links: false`.
- Actual insertion, removal, replacement, anchor change, or placement change sets it to true.

### T-A1-013 Template default recalculation

Expected:

The following fields are explicitly recalculated:

- `improvement_type`
- `confidence`
- `next_action`
- `recommended_review_days`

A copied default without reassessment fails validation.

### T-A1-014 Confidence rules

Expected:

- Estimated main query prevents high confidence.
- Blocking error forces invalid output.
- Graceful degradation may remain high only when missing data does not affect the core recommendation.

### T-A1-015 new_values scope

Expected:

Only these keys are allowed:

- `article_title`
- `seo_title`
- `description`
- `main_query`

Missing introduction, body, FAQ, or link values are not contract violations.

### T-A1-016 Summary consistency

Expected:

- Summary statements match the change flags.
- Preserved targets are not described as rewritten.
- Changed targets are not described as preserved.

## 4. Negative test fixtures to add

Create synthetic invalid fixtures for:

1. Missing required field
2. Invalid enum
3. `information` as object
4. `changes.body` as string
5. Unknown change key
6. ArticleID mismatch
7. URL mismatch
8. Estimated query without `estimated_fields`
9. `internal_links: false` with an inserted link
10. `body: false` with a rewritten H2 section
11. `confidence: high` with a high-severity warning
12. Unregistered warning code
13. Template default recalculation omitted

## 5. Pass criteria

Phase A1 passes when:

- Baseline valid JSON parse rate: 100%
- Required-field error after normalization: 0
- Enum error: 0
- Type error: 0
- Unknown change key: 0
- Article identity conflict detection: 100%
- Change-flag contradiction detection: 100%
- Warning-code registration: 100%
- Template default recalculation: 100%
- SIMS-Blog-Manager external compatibility: preserved

## 6. Test reporting format

Each test run records:

```json
{
  "fixture": "A000369.txt",
  "schema_valid": true,
  "semantic_valid": true,
  "blocking_errors": [],
  "warning_codes": [],
  "normalized_fields": [],
  "result": "PASS"
}
```

Allowed results:

- `PASS`
- `PASS_WITH_NORMALIZATION`
- `FAIL_SCHEMA`
- `FAIL_SEMANTIC`
- `BLOCKED_IDENTITY_CONFLICT`
