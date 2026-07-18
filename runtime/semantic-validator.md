# SIMS Writer Semantic Validator

Version: 1.0.0  
Dependency: `runtime/contract-validation.md`

## 1. Purpose

The semantic validator detects output that satisfies the JSON shape but contradicts the actual analysis or delivered edits.

It runs after schema validation and before final JSON emission.

## 2. Required internal state

Before final validation, SIMS Writer must internally determine:

- request ArticleID
- request URL
- selected main query
- main query source
- missing inputs
- whether the body was inspected
- whether body changes were required
- actual changed targets
- actual delivered replacement values
- warning codes and severities
- improvement scope
- recommended next action

## 3. Validation rules

### SV-001 Article identity

Condition:

- Output `article_id` differs from the request, or
- Output `article_url` differs from the request, or
- A known ArticleID-to-URL mapping conflicts with the output.

Result:

- Add `WC_ARTICLE_ID_URL_MISMATCH` with severity `blocking`.
- Stop final output registration.

### SV-002 Main-query source

Rules:

- Explicit request query requires `manual`.
- Search Console selection requires `search_console`.
- Content inference requires `estimated`.
- `estimated` requires `estimated_fields` to contain `main_query`.
- `manual` and `search_console` must not list `main_query` as estimated.

### SV-003 Execution mode

Use `standard` when all inputs required for the selected analysis are present.

Use `graceful_degradation` when a missing input prevents part of the normal analysis but does not invalidate the safe remaining work.

When graceful degradation is used:

- Missing inputs must be recorded internally.
- A human-readable explanation must appear in `information`.
- Confidence is reduced only when the missing input materially affects the recommendation.

### SV-004 Change flags

For every change target:

```text
actual modification exists => changes.<target> = true
no actual modification      => changes.<target> = false
```

The validator compares:

- Before/After sections
- completed article output
- summary
- internal actual-change list
- `changes`

Contradiction code:

```text
WC_CHANGE_FLAG_MISMATCH
```

### SV-005 Introduction versus body

- Changes before the first H2 belong to `introduction`.
- Changes under an H2 belong to `body`.
- A modified H2 label belongs to `headings`.
- A paragraph immediately following a changed H2 is still body text.

### SV-006 Internal links

Set `internal_links: true` only when at least one link is actually changed.

The following do not count as changes:

- candidate evaluation
- candidate rejection
- recommendation without insertion
- repeating an existing link unchanged

Suspected self-links or mismatched catalog entries add the appropriate warning code.

### SV-007 Images

Set `images: true` only when image content, image placement, alt text, caption, or image instruction is actually changed.

Missing image data alone does not set `images: true`.

### SV-008 new_values

The validator confirms:

- changed management fields have the final intended value
- unchanged management fields do not contain an invented replacement
- `main_query` matches the selected query
- no unsupported key is added

### SV-009 Improvement type

Recalculate after changes are finalized.

Suggested decision rules:

#### minor

- one or two narrowly scoped changes
- no body rewrite
- no search-intent restructuring
- low implementation effort

#### normal

- several coordinated changes
- title, introduction, headings, FAQ, or links are adjusted
- body is mostly preserved or locally edited

#### major

- broad body rewrite
- search-intent correction across the article
- major structural reorganization
- rewrite is required to resolve a serious mismatch

The template value must never be accepted without recalculation.

### SV-010 Confidence

#### high

Allowed only when:

- Article identity is verified.
- The main query is not estimated.
- Major input data is available.
- The body was inspected where body judgment is made.
- No high-severity uncertainty remains.
- Missing inputs do not affect the core recommendation.

#### medium

Required as an upper bound when:

- the main query is estimated
- Search Console sample size is small
- year, price, specification, or other changing fact needs confirmation
- an important input is missing
- search diagnosis has material uncertainty

#### low

Required when:

- the body was unavailable for a body-level judgment
- Article identity is unresolved
- a blocking contract error exists
- a major factual issue remains unresolved
- the recommendation cannot be made reliably

### SV-011 Warning and confidence relationship

Warnings do not automatically force low confidence.

The validator uses severity:

- `info`: no mandatory reduction
- `low`: usually no mandatory reduction
- `medium`: confidence cannot be high when it affects the core recommendation
- `high`: confidence cannot exceed medium
- `blocking`: final output cannot be registered

### SV-012 next_action

Recalculate after the final plan:

#### monitor

Use when no immediate edit is required and performance should be observed.

#### remeasure

Use after a concrete improvement has been applied and future Search Console measurement is appropriate.

#### rewrite

Use when the article requires a broad rewrite that is not safely completed in the current response, or when the selected output mode explicitly defers it.

#### none

Use only when no follow-up is required.

A response that actually changes content will normally use `remeasure`, not `monitor`.

### SV-013 Recommended review days

Suggested rules:

- `7`: urgent or fast-moving correction, or an early validation check
- `14`: normal post-improvement remeasurement
- `30`: low-volume query, slow-moving article, or insufficient early sample size

The value must be justified by the diagnosis and must not simply remain at the template default.

### SV-014 Summary consistency

The summary must accurately state:

- what was changed
- what was preserved
- any material limitation
- the intended effect

The summary must not claim a body rewrite when `body` is false, or claim no internal-link change when `internal_links` is true.

### SV-015 Template default prevention

Before output, the runtime must explicitly recalculate:

- `improvement_type`
- `confidence`
- `next_action`
- `recommended_review_days`

The validator records:

```json
"template_defaults_recalculated": true
```

If this step was skipped, output is invalid.

## 4. Final semantic decision

The final JSON may be emitted only when:

- no blocking semantic error remains
- every change flag matches delivered content
- identity is verified
- enum choices are justified
- warning codes are registered
- decision fields were recalculated

## 5. Validation order

1. Identity
2. Main query and source
3. Missing input and execution mode
4. Actual changed targets
5. Change flags
6. New values
7. Warning generation
8. Improvement type
9. Confidence
10. Next action
11. Review days
12. Summary consistency
13. Final schema validation
