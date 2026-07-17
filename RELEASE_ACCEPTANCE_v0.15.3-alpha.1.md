# Release Acceptance — v0.15.3-alpha.1

## Base verification

- Source repository: user-provided `SIMS-Writer(2).zip`
- Confirmed source version: `0.15.0-alpha.1`
- Previous generated package discrepancy reviewed
- Project Instructions and Knowledge Pack are now version-aligned

## Root cause fixed

1. Knowledge Pack remained at `0.14.3-alpha.1` and instructed estimated queries to be warnings.
2. Project Instructions treated the request's legacy `SIMS_FEEDBACK_V1` v1.1 sample as an immutable contract, suppressing v1.2 fields.

## Release gates

- Claude asset consistency tests: 5 passed
- Related runtime and output tests: 20 passed total
- Golden UAT: 12/12 passed
- Contract examples: 15/15 passed
- ZIP CRC verification: required before delivery

## Expected A000008 feedback metadata

```json
{
  "version": "1.2",
  "main_query_source": "estimated",
  "execution_mode": "graceful_degradation",
  "estimated_fields": ["main_query"],
  "warnings": [],
  "information": [
    "main_queryを記事タイトル・本文から推定して処理しました。",
    "article_catalogが未入力のため、内部リンク候補の選定のみSKIPしました。"
  ]
}
```
