# SEO Critical Auto Repair Validation

## Required checks

- Critical and advisory findings are classified separately.
- Advisory-only findings never produce `PUBLIC_BLOCKED`.
- A critical finding triggers a repair attempt before user output.
- The repaired candidate is revalidated.
- The loop is capped at three cycles.
- Public output contains the final candidate, never the rejected draft.
- Genuine user decisions include a blocking flag.
- Future optional updates do not block current publication.

## Canonical codes

- `VAL-SEO-CRITICAL-CLASSIFICATION`
- `VAL-AUTO-REPAIR-EXECUTION`
- `VAL-REVALIDATION-CYCLE`
- `VAL-FINALIZATION-GATE`
- `VAL-NONBLOCKING-FOLLOWUP-SEPARATION`
