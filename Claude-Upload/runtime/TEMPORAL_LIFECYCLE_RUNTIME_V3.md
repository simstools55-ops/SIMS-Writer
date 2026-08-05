# Stage 05A: Temporal Lifecycle Analysis

Run after Knowledge Assembly and before Content Planning when temporal triggers exist.

## Inputs
- current date and evidenced source dates
- article title/meta/body/table/FAQ/CTA
- official/current source state
- Search Console and SERP demand context

## Outputs
- lifecycle_status: ANNOUNCED | SCHEDULED | ACTIVE | COMPLETED | EXPIRING | EXPIRED | ARCHIVED | UNKNOWN
- previous_lifecycle_status when inferable
- temporal_shift_detected
- stale_components
- contradictions
- preservation_signals
- recommended_scope

## Rules
- Search demand cannot verify facts.
- A phase change is not an automatic full rewrite.
- Unresolved material contradictions cannot be PUBLIC_OK.
- Historical context may remain when clearly framed and useful.
