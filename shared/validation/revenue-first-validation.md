# Revenue First Validation and Auto Repair v3.1.0

## Validation tiers

### TIER 1 — REVENUE_OR_SAFETY_CRITICAL
Blocks publication until repaired:

- material factual or safety error;
- primary-intent mismatch;
- winner-query asset destruction;
- material CTR/title regression risk without supporting evidence;
- title/meta/body promise mismatch;
- broken link, self-reference error or unresolved cannibalization;
- Contract, Before/After, new_values or JSON mismatch.

### TIER 2 — AUTO_REPAIR
Repair internally and revalidate:

- unsupported superlative or freshness label;
- over-broad causal or universal claim;
- incomplete FAQ wording that changes reader action;
- stale mutable value that can be safely removed or qualified;
- fixable internal-link or synchronization defect.

### TIER 3 — NON_BLOCKING_QUALITY
Do not block publication or create user decision:

- stylistic preference;
- punctuation or minor tone refinement;
- optional supporting detail;
- optional FAQ or link opportunity;
- a safer alternative that does not materially change truth, intent or SEO performance.

## Auto-repair loop

Draft → Revenue First Validation → smallest safe repair → revalidation, up to three cycles.

If Tier 1 remains after the repair budget, output PUBLIC_BLOCKED internally. User-facing output must contain only final PUBLIC_OK changes and genuine user-owned decisions.

## CTR rule

CTR improvement is evaluated through query demand, ranking position, snippet alignment and intent fit. Unsupported numerical CTR or click forecasts are prohibited.
