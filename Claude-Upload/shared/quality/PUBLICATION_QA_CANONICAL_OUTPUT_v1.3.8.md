# Publication QA Canonical Output v1.3.8

## Machine contract

- `changes[].component` only; no `target`.
- `meta_description` only; no `description` or `seo_description`.
- `publication_qa.contract = SIMS_EDITORIAL_QA_V1`.
- `auto_fixes`, `review_trace`, and `unresolved_findings` are structured arrays.
- Empty strings are forbidden. Omit unknown optional values.
- Unchanged components never appear in `changes[]`.
- Candidate-level internal-link decisions belong in `internal_link_evaluation`.
- An unresolved finding forbids final `PASS`; use `PASS_WITH_WARNING` when publishable.

## Reviewer precision

Without explicit evidence, do not publish absolute, causal, generalized numeric, or subjective claims such as complete coverage, guaranteed resolution time, universal multipliers, fixed usage percentages, or claims that different errors are the same.

## User-facing language

Use Japanese labels in prose. Show the English code only at first use, in parentheses. Keep machine codes unchanged inside JSON.
