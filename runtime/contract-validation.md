# SIMS Writer Contract Validation

Version: 1.0.0  
Applies to: `SIMS_FEEDBACK_V2` version `1.2`

## 1. Purpose

This specification validates the final SIMS Writer feedback JSON before it is returned to SIMS-Blog-Manager.

The validator has two responsibilities:

1. Confirm that the output satisfies the external JSON contract.
2. Prevent structurally valid but semantically contradictory output.

The external contract remains backward compatible with `SIMS_FEEDBACK_V2` version `1.2`.

## 2. Validation sequence

Validation must run in this order:

1. Normalize non-semantic formatting.
2. Run schema validation.
3. Run semantic validation.
4. Recalculate decision fields.
5. Run final consistency validation.
6. Return JSON only when no blocking error remains.

A formatter must never silently repair a semantic decision.

## 3. Required top-level fields

The following fields are mandatory:

- `format`
- `version`
- `article_id`
- `article_url`
- `completed_at`
- `changes`
- `new_values`
- `main_query_source`
- `execution_mode`
- `estimated_fields`
- `improvement_type`
- `confidence`
- `expected_effect`
- `next_action`
- `summary`
- `warnings`
- `information`
- `estimated_minutes`
- `recommended_review_days`

## 4. Fixed values

### 4.1 Format

```json
"format": "SIMS_FEEDBACK_V2"
```

### 4.2 Version

```json
"version": "1.2"
```

A different value is a blocking contract error.

## 5. Enumerations

### 5.1 main_query_source

Allowed values:

- `manual`
- `search_console`
- `estimated`

Rules:

- Use `manual` when the request explicitly supplies the main query.
- Use `search_console` when SIMS Writer selects it from supplied Search Console query data.
- Use `estimated` only when it is inferred from article content or titles.
- When `estimated` is used, `estimated_fields` must include `main_query`.

### 5.2 execution_mode

Allowed values:

- `standard`
- `graceful_degradation`

Use `graceful_degradation` only when one or more inputs are missing or incomplete and the analysis can still safely continue.

The missing input must be recorded in `information` and in the internal validation state.

### 5.3 improvement_type

Allowed values:

- `minor`
- `normal`
- `major`

This value must be recalculated after all changes are known. It must not be copied from a template default.

### 5.4 confidence

Allowed values:

- `high`
- `medium`
- `low`

This value must be recalculated after warnings, missing inputs, and estimated fields are known.

### 5.5 next_action

Allowed values:

- `monitor`
- `remeasure`
- `rewrite`
- `none`

This value must be recalculated after the final improvement decision.

### 5.6 recommended_review_days

Allowed values:

- `7`
- `14`
- `30`

## 6. changes contract

`changes` must contain all and only the following boolean keys:

```json
{
  "article_title": false,
  "seo_title": false,
  "description": false,
  "introduction": false,
  "headings": false,
  "faq": false,
  "internal_links": false,
  "body": false,
  "images": false
}
```

A key is `true` only when the final response actually changes that target.

Evaluating an item without modifying it does not set the flag to `true`.

### 6.1 Introduction and body boundary

- Text before the first H2 belongs to `introduction`.
- Text at or after the first H2 belongs to `body`.
- Editing only the pre-H2 text means `introduction: true` and `body: false`.

### 6.2 Internal links

`internal_links` is `true` only when a link is added, removed, replaced, or its anchor text or placement is changed.

Reviewing candidates and rejecting all of them leaves `internal_links: false`.

## 7. new_values contract

`new_values` stores only management values consumed by SIMS-Blog-Manager.

Allowed keys:

- `article_title`
- `seo_title`
- `description`
- `main_query`

It is not a complete record of every changed passage.

If a corresponding field is unchanged, preserve the established contract convention used by the current adapter. Do not invent new keys.

## 8. Array and object types

### 8.1 estimated_fields

Must be an array of strings.

### 8.2 warnings

Must be an array of strings in the following external form:

```text
WARNING_CODE: Human-readable Japanese message
```

Example:

```json
"warnings": [
  "WC_LOW_SAMPLE_SIZE: 表示回数が少なく、判断の確度に限界があります。"
]
```

Internally, warnings may be structured objects, but the output adapter converts them to strings for backward compatibility.

### 8.3 information

Must always be an array of strings.

Correct:

```json
"information": [
  "画像データが未提供のため、画像評価は行っていません。"
]
```

Incorrect:

```json
"information": "画像データが未提供です。"
```

## 9. Article identity validation

The pair `article_id` and `article_url` must exactly match the request.

The validator must also reject a known mapping in which one ArticleID is associated with a different URL.

Blocking warning code:

```text
WC_ARTICLE_ID_URL_MISMATCH
```

When this occurs:

- Contract validation fails.
- Quality evaluation is not finalized.
- The output must not be registered in SIMS-Blog-Manager.

## 10. Permitted automatic normalization

The validator may automatically normalize:

- surrounding whitespace
- array initialization to `[]`
- missing false values inside an otherwise valid `changes` object
- integer conversion for numeric integer fields
- warning string formatting when code and message are already known

The validator must not automatically decide or overwrite:

- `article_id`
- `article_url`
- `main_query_source`
- change flags based on guesswork
- `improvement_type`
- `confidence`
- `next_action`
- factual claims

## 11. Blocking conditions

Do not emit the final JSON when any of the following remains:

- invalid JSON
- missing required field
- unknown top-level key that conflicts with the contract
- invalid enum
- invalid field type
- ArticleID and URL mismatch
- change flag and delivered output contradiction
- estimated main query without `estimated_fields`
- unresolved semantic contradiction

## 12. Internal validation result

The runtime keeps the following internal state. It is not normally shown to the user.

```json
{
  "schema_valid": true,
  "semantic_valid": true,
  "auto_fixed": false,
  "blocking_errors": [],
  "warning_codes": [],
  "body_checked": true,
  "body_change_required": false,
  "main_query_source_verified": true,
  "template_defaults_recalculated": true
}
```

## 13. Completion criteria

Phase A1 schema validation passes when:

1. Every regression fixture parses as JSON.
2. Required-field omission count is zero.
3. Enum violation count is zero.
4. Type violation count is zero.
5. `information` is always an array.
6. `warnings` is always an array.
7. Article identity mismatches are detected.
8. No unsupported change key is emitted.
9. The final output remains compatible with SIMS-Blog-Manager.
