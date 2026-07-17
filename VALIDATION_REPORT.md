# Validation Report

Version: 0.15.1-alpha.1
Status: Graceful Degradation Alpha

## Automated checks

- Targeted pytest regression suite: 20 passed
- Contract schema examples: 15 passed, 0 failed
- Golden UAT: 12 passed, 0 failed
- Runtime graceful-degradation checks: passed
- RC2 Strict Contract regression retained

## RC3 scope

- Three-level improvement necessity judgment
- Search-intent classification
- Comparison article consistency validation
- Expected-effect requirement for changed items
- Unchanged-reason rule
- Estimated editing time

## Known boundary

- `partial` remains the Product 1.0 primary mode.
- `full` and `publish` remain beta.
- Comparison consistency validation requires structured comparison data; Claude Instructions provide the human-output gate.

## 0.15.1 scope

- Missing `main_query` no longer causes a fatal stop.
- Missing `article_catalog` skips internal-link selection only.
- Source and optional-input shortages are warnings where processing can continue.
- `manual_review_required` remains reserved for genuinely blocking human review.
