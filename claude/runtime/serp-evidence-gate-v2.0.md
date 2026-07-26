# SERP Evidence Gate v2.2

This gate runs before Editorial Planner whenever the main-query average position is greater than 3.0.

## Gate result
- `OPEN`: `serp_analysis_status=verified`; all components may proceed subject to Evidence and QA.
- `PROGRESSIVE`: `serp_analysis_status=partial`; send each component to Progressive Editing Engine instead of stopping the article.
- `LIMITED`: `serp_analysis_status=unavailable`; only non-SERP mechanical or authoritative factual corrections may continue.

## Non-bypass rule
Search Console queries, article completeness, LOW_SAMPLE, user urgency, or a plausible improvement idea cannot substitute for current result-page inspection. Partial inspection is useful evidence, but it must be applied only within its verified scope.

## Audit fields
Retain `serp_analysis_status`, `serp_checked_at`, `usable_result_count`, `verified_scope`, `component_decisions`, `blocked_change_types`, and `evidence_sources` internally. Do not expose the gate trace to the normal user.
