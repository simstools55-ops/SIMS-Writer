# SERP Analysis Engine v2.1

## Purpose
Before deciding edits, reconstruct the search intent currently represented in the top search results and compare it with the target article.

## Mandatory trigger
When the supplied average position for the main query is greater than 3.0, a current top 10 organic-result inspection is a blocking prerequisite for search-intent, competitor-gap, heading, FAQ, body-expansion, structural, and title-repositioning edits.

Exceptions are limited to:
- an explicit emergency factual or safety correction;
- a purely mechanical defect that does not depend on search intent;
- an exact correction of a verified factual contradiction already visible in the supplied article;
- a valid, same-date SERP evidence package supplied by the user.

## Required status
Set one internal status before planning:
- `verified`: sufficient current result pages were inspected;
- `partial`: some pages were inspected, but the evidence is insufficient for a reliable top-10 comparison;
- `unavailable`: current result pages could not be inspected.

`partial` and `unavailable` are blocking for SERP-dependent edits. They are not warnings that permit the same edits to continue.

## Required observations
For each usable top result, record only verifiable observations:
- result URL/domain and title;
- dominant intent and answer type;
- material headings/topics;
- concrete facts, tables, procedures, examples, images or official-source use;
- freshness signals where visible;
- distinctive value, not just word count.

## Unverified-SERP whitelist
When status is `partial` or `unavailable`, only the following may be placed in `PUBLIC_OK`:
- typographical, encoding, formatting or broken-markup correction;
- removal of demonstrably unrelated accidental text, when deletion is unambiguous;
- correction of an internally contradictory statement using facts already verified in the supplied article;
- legal, safety or factual correction supported by authoritative evidence;
- restoration of missing metadata caused by a mechanical truncation, without changing the search promise.

The following are prohibited from `PUBLIC_OK` until status is `verified`:
- new FAQ entries;
- new headings or heading-intent changes;
- body expansion, deletion, reordering or structural changes;
- competitor-gap claims;
- adding secondary-query topics merely because query rows exist;
- changing the title promise or primary intent positioning;
- claims that current top results commonly cover a topic.

## Required behavior when blocked
- Do not generate a substitute competitor analysis from Search Console query rows.
- Do not infer result-page content from snippets alone.
- Do not fabricate SERP findings or generalize unavailable evidence.
- Record the blocked plan internally.
- In the user view, do not expose diagnosis codes or detailed QA. State only that current top-result comparison could not be completed and that SERP-dependent edits were therefore withheld.
- If no whitelist correction exists, return no publication change rather than a speculative edit.
