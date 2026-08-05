# Progressive Editing Engine v2.0

The engine runs after Evidence Layer and before final Editorial Decision.

## Purpose
Do not stop the entire article when only part of the evidence or SERP inspection is incomplete. Determine the maximum safe progress separately for title, meta description, introduction, headings, FAQ, body, structure, images and internal links.

## SERP verification levels
- `verified`: full component planning is available, subject to Evidence and QA.
- `partial`: inspected results provide useful but incomplete coverage. Component-scoped editing is allowed.
- `unavailable`: only non-SERP mechanical or authoritative factual corrections may progress.

## Partial-mode matrix
- SEO title / meta description / introduction: may be `PUBLIC_OK` when they faithfully summarize the current article, use supported claims, and do not introduce an unverified competitor gap or new search promise.
- Heading / FAQ / body / structure: may be `USER_DECISION` when the gap is plausible and supported but top-result coverage is incomplete. Otherwise `INTERNAL_REJECT`.
- Mechanical fixes, accidental-text removal, verified contradiction fixes and non-promissory truncation repair: may be `PUBLIC_OK`.
- LOW evidence: always `USER_DECISION`; NONE: always `INTERNAL_REJECT`.

## Scope rule
SERP status applies to each proposed component, not to the article as a whole. One blocked body edit must not suppress a safe meta correction. One verified title edit must not authorize an unsupported FAQ.

## Output rule
The user sees completed `PUBLIC_OK` edits first and only actionable `USER_DECISION` items afterward. Held items remain internal. Do not expose the progressive matrix, evidence scores or gate codes.
