# SERP Evidence Gate v2.0

This gate runs before Editorial Planner whenever the main-query average position is greater than 3.0.

## Gate result
- `OPEN`: `serp_analysis_status=verified`; SERP-dependent planning may continue.
- `LIMITED`: status is `partial` or `unavailable`; only the unverified-SERP whitelist may continue.
- `BLOCKED`: the proposed change is SERP-dependent and status is not `verified`; classify the proposal as `INTERNAL_REJECT`.

## Non-bypass rule
Search Console queries, article completeness, LOW_SAMPLE, user urgency, or a plausible improvement idea cannot substitute for current result-page inspection.

## Audit fields
The internal audit record must retain:
- `serp_analysis_status`;
- `serp_checked_at`;
- `usable_result_count`;
- `blocked_change_types`;
- `allowed_non_serp_changes`;
- `evidence_sources`.

These fields remain internal and are not shown in the normal user response.
