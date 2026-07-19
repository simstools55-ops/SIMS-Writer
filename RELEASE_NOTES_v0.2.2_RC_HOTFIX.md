# SIMS Writer v0.2.2 RC Hotfix

## Purpose

Applies findings from 11 real-article regression tests.

## P0 fixes

- Enforces SIMS_FEEDBACK_V2 v2.0 and rejects legacy V1 output.
- Adds article ID/URL and answer-consistency validation.
- Removes raw HTML Before/After wrappers; uses wrapping Markdown blockquotes.
- Adds title-promise/body-fulfillment checks.

## P1 quality fixes

- Adds main-query overfit, rank-causality, named-person attribution, food safety, privacy redaction, app freshness/free-scope, language/etymology, and earnings validation.
- Prevents unsupported featured-snippet, FAQ-rich-result, voice-search, and guaranteed CTR claims.
- Distinguishes preserved internal links from held candidates.

## Regression coverage

Eleven real-article cases are registered in `tests/rc-hotfix-v0.2.2/`.
