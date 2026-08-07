# SEO Critical Auto Repair Runtime v3.0.1

## Runtime pipeline

Input → Analysis → Editing Plan → Draft Changes → SEO Critical Validation → Auto Repair → Revalidation → Publication Finalization Gate → Contract 4.2 JSON

## Operating rule

The runtime must return a publication-ready candidate whenever a safe local repair is possible. It must not stop publication for editorial perfection issues with negligible SEO impact.

## Repair priority

1. Preserve search intent and winner-query assets.
2. Remove or soften unsupported central claims.
3. Repair title/meta/body promise inconsistencies.
4. Remove unverified mutable values or replace them with a verification path.
5. Repair HTML and JSON synchronization.
6. Reduce the editing budget rather than performing a risky rewrite.

## Loop limit

Maximum three review cycles. If an SEO-critical problem survives, return `PUBLIC_BLOCKED` together with the best safe replacement text that could be produced.
