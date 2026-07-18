# SIMS Writer Warning Code Registry

Version: 1.0.0

## 1. Purpose

This registry is the Single Source of Truth for warning codes used by SIMS Writer.

The model must not invent a new warning code during normal execution. A new code requires a controlled specification update.

## 2. External format

Warnings are returned as strings for compatibility with SIMS-Blog-Manager:

```text
CODE: Japanese message
```

Example:

```json
"warnings": [
  "WC_LOW_SAMPLE_SIZE: 表示回数が少ないため、改善効果の判断には追加測定が必要です。"
]
```

## 3. Severity levels

- `info`: supplemental information
- `low`: minor concern
- `medium`: meaningful uncertainty or review recommendation
- `high`: significant risk requiring review
- `blocking`: output must not be registered

## 4. Contract and identity warnings

### WC_ARTICLE_ID_URL_MISMATCH

Severity: `blocking`

Use when the ArticleID and URL do not match the request or known article mapping.

### WC_SCHEMA_REQUIRED_FIELD

Severity: `blocking`

Use when a required output field is missing.

### WC_SCHEMA_INVALID_TYPE

Severity: `blocking`

Use when a field has the wrong JSON type.

### WC_SCHEMA_INVALID_ENUM

Severity: `blocking`

Use when an unapproved enum value is used.

### WC_SCHEMA_UNKNOWN_KEY

Severity: `high`

Use when an unsupported output key is added and cannot be safely ignored.

### WC_CHANGE_FLAG_MISMATCH

Severity: `blocking`

Use when `changes` contradicts the actual delivered modifications.

### WC_EXECUTION_MODE_MISMATCH

Severity: `high`

Use when `execution_mode` does not reflect missing inputs or analysis conditions.

### WC_CONFIDENCE_MISMATCH

Severity: `high`

Use when confidence is materially higher than the available evidence supports.

### WC_TEMPLATE_DEFAULT_NOT_RECALCULATED

Severity: `blocking`

Use when a decision field appears to have been copied from the template without final reassessment.

## 5. Input and analysis warnings

### WC_MAIN_QUERY_ESTIMATED

Severity: `medium`

Use when the main query is inferred rather than supplied or selected from Search Console data.

### WC_LOW_SAMPLE_SIZE

Severity: `medium`

Use when Search Console impressions or clicks are too limited for a confident diagnosis.

### WC_LOW_RANK_VISIBILITY

Severity: `low`

Use when the average position is too low for CTR conclusions to be reliable.

### WC_INPUT_ARTICLE_CATALOG_MISSING

Severity: `low`

Use when an article catalog required for internal-link evaluation is unavailable.

### WC_INPUT_IMAGE_DATA_MISSING

Severity: `info`

Use when image data is unavailable and image evaluation is skipped.

### WC_BODY_NOT_AVAILABLE

Severity: `high`

Use when a body-level judgment is requested but the article body cannot be inspected.

## 6. Content warnings

### WC_CONTENT_HEADING_MISMATCH

Severity: `medium`

Use when a heading and the content beneath it do not match.

### WC_BODY_CONTRADICTION

Severity: `high`

Use when important statements within the article contradict one another.

### WC_NAMING_INCONSISTENCY

Severity: `low`

Use when product, service, person, or feature naming is inconsistent.

### WC_STRONG_CLAIM

Severity: `medium`

Use when a strong or absolute claim requires support or softer wording.

### WC_FACT_CHECK_REQUIRED

Severity: `medium`

Use when a factual statement should be checked before publication.

### WC_UNSUPPORTED_STATEMENT

Severity: `medium`

Use when a claim lacks a confirmable basis.

### WC_YEAR_DEPENDENT

Severity: `medium`

Use for information that may change by year, including prices, rules, versions, and schedules.

### WC_FIRST_PERSON_UNVERIFIED

Severity: `high`

Use when the output invents personal experience not supplied by the user or source article.

## 7. Internal-link warnings

### WC_INTERNAL_LINK_DATA_MISMATCH

Severity: `medium`

Use when a candidate title, URL, or article identity conflicts with the supplied catalog.

### WC_INTERNAL_LINK_LOW_RELEVANCE

Severity: `low`

Use when a candidate is only weakly related to the article or search intent.

### WC_SELF_LINK_SUSPECTED

Severity: `medium`

Use when an internal-link candidate appears to point to the article itself.

## 8. Warning selection rules

- Use the smallest number of warnings necessary.
- Do not emit multiple codes for the same issue unless they represent distinct risks.
- Do not add a warning merely because an optional improvement exists.
- Warnings describe uncertainty, risk, or contract conditions—not ordinary editing suggestions.
- Every warning message must identify the affected issue and recommended action when useful.

## 9. Confidence relationship

- `blocking`: output cannot be registered
- `high`: confidence cannot exceed `medium`
- `medium`: confidence cannot be `high` when the warning affects the main recommendation
- `low` or `info`: no automatic reduction unless several warnings combine into material uncertainty
