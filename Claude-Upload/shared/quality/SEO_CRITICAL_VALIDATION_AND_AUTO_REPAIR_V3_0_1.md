# SEO Critical Validation and Auto Repair v3.0.1

## Purpose

Validation exists to prevent SEO loss, unsafe publication, and broken output. It must not turn minor prose polishing into a publication blocker.

## Two classes

### SEO_CRITICAL
Publication is held only when one or more of the following remain after repair:

- primary search intent is materially broken;
- a claim could cause serious reader harm;
- spam or deceptive optimization could materially reduce Google trust;
- title/meta promises materially exceed article delivery;
- a change could destroy a winning page or protected asset;
- page-breaking HTML or Contract/JSON corruption remains;
- a central, mutable or numeric claim is published as confirmed without sufficient evidence.

### QUALITY_RECOMMENDATION
These do not block publication by themselves:

- small wording and tone refinements;
- minor evidence wording calibration without material reader risk;
- sentence-length, punctuation or style consistency;
- optional FAQ/internal-link opportunities;
- other changes with negligible expected SEO impact.

## Mandatory repair loop

1. Generate the SEO improvement candidate.
2. Run SEO Critical Validation.
3. Apply the smallest safe repair.
4. Re-run validation.
5. Repeat up to three cycles.
6. Package only the final reviewed candidate.

The user should not be used as the repair engine. A blocker is shown only when the system cannot safely repair it or the choice genuinely belongs to the user.

## Publication states

- `PUBLIC_OK`: all blocking defects are resolved.
- `PUBLIC_OK_WITH_USER_DECISION`: safe changes are ready; only genuine user-owned decisions remain. Each decision must declare `blocking`.
- `PUBLIC_BLOCKED`: an SEO-critical defect remains after the repair budget is exhausted.

Non-blocking future updates belong in follow-up actions or warnings, not blocking user decisions.
