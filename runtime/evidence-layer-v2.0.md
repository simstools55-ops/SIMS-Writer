# Evidence Layer v2.0

Evidence Layer runs after Search Console and SERP analysis and before Gap Analysis and Editorial Planner.

## Purpose
A proposed edit may become `PUBLIC_OK` only when every material factual claim in that edit is supported strongly enough for direct publication. Search demand and competitor prevalence are not factual proof.

## Evidence dimensions
For each proposed claim or edit, record:
- `query_signal`: whether Search Console shows reader demand;
- `serp_signal`: whether verified top results materially cover the topic;
- `primary_evidence`: official or first-party support;
- `secondary_evidence`: reliable independent support;
- `article_evidence`: whether the current article already contains the fact;
- `freshness_status`: current, stale, unknown, or not_applicable;
- `evidence_level`: HIGH, MEDIUM, LOW, or NONE.

## Decision mapping
- `HIGH`: may be `PUBLIC_OK` after normal QA.
- `MEDIUM`: may be `PUBLIC_OK` only for low-risk wording that does not overstate the evidence; otherwise `USER_DECISION`.
- `LOW`: must be `USER_DECISION`; it cannot appear inside any `PUBLIC_OK` edit.
- `NONE`: `INTERNAL_REJECT`.

## Non-substitution rule
The following cannot substitute for factual evidence:
- Search Console query frequency;
- repetition across unverified pages;
- plausible technical explanations;
- an existing unsourced statement in the article;
- model memory.

## Cross-change contamination rule
A claim classified as LOW or NONE must not appear in a title, meta description, introduction, heading, FAQ, or body edit classified as `PUBLIC_OK`. If it does, Publication QA blocks the entire contaminated change.

## Audit output
Store the evidence matrix and contamination findings only in the internal audit record. The normal user output shows evidence details only when a `USER_DECISION` needs a concrete confirmation point.
