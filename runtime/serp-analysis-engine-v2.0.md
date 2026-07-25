# SERP Analysis Engine v2.0

## Purpose
Before deciding edits, reconstruct the search intent currently represented in the top search results and compare it with the target article.

## Mandatory trigger
When the supplied average position for the main query is greater than 3.0, analyze the current top 10 organic results before selecting the change scope.

Exceptions are limited to:
- an explicit emergency factual/safety correction;
- a purely mechanical defect whose correction does not depend on search intent;
- the user explicitly supplies a verified SERP analysis package created on the same date.

## Required observations
For each usable top result, record only verifiable observations:
- result URL/domain and title;
- dominant intent and answer type;
- material headings/topics;
- concrete facts, tables, procedures, examples, images or official-source use;
- freshness signals where visible;
- distinctive value, not just word count.

## Prohibitions
- Do not copy wording or structure mechanically.
- Do not infer the full content from snippets alone.
- Do not treat frequency as proof of correctness.
- Do not fabricate SERP findings when browsing or supplied evidence is unavailable.

## Unavailable SERP behavior
If position >3 and current top-result content cannot be inspected, set `serp_analysis_status=unavailable`. Do not approve content-expansion, FAQ, heading, or structural edits whose justification depends on competitor gaps. Mechanical/factual corrections may proceed independently.
