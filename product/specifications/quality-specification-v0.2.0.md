# SIMS Writer Quality Specification v0.2.0

Status: Quality Freeze  
Basis: 10-article real-content regression test  
Scope: Existing-article improvement (`partial`) is the production default.

## 1. Product quality objective

SIMS Writer is an editor for existing articles, not a full-rewrite generator by default. It must improve the smallest justified set of components while preserving proven value, search intent, monetization elements, and original experience.

## 2. Decision order

1. Validate required input and identify unavailable evidence.
2. Determine primary search intent; add a secondary intent only when it changes structure or conclusion.
3. Diagnose search performance using impressions, CTR, average position, query distribution, and sample size together.
4. Identify protected elements and preservation signals.
5. Decide whether change is needed.
6. Set Rewrite Level, Rewrite Scope, Change Budget, and risk before drafting.
7. Produce only approved changes.
8. Run Validation Layer and repair targeted defects.
9. Package human output and machine feedback separately.

## 3. Improvement necessity

- `IMPROVEMENT_RECOMMENDED`: Clear opportunity or mismatch requiring a concrete change.
- `MINOR_IMPROVEMENT`: Article is fundamentally sound; limited refinement is justified.
- `KEEP_CURRENT`: Evidence does not justify a change, or risk exceeds expected value.

A low CTR alone never proves that the title is the cause.

## 4. Diagnosis codes

- `POSITION_OPPORTUNITY`: Usually position 4–12 with meaningful impressions and CTR below the position/context expectation. Prioritize title, introduction, and SERP promise alignment before body expansion.
- `CONTENT_OPPORTUNITY`: Usually position 10.1–20 or query coverage indicates insufficient content alignment.
- `LOW_SAMPLE`: Insufficient impressions for a reliable performance judgment. Avoid aggressive changes and recommend remeasurement.
- `STRONG_CURRENT_PERFORMANCE`: Current performance and content alignment do not justify change.
- `INTENT_MISMATCH`: Title, introduction, headings, body, or conclusion does not satisfy the primary intent.
- `EVIDENCE_GAP`: A material factual or time-sensitive claim cannot be verified.
- `INPUT_INCOMPLETE`: Required content or contract data is unavailable.

`LOW_SAMPLE` may coexist with another diagnosis, but it lowers confidence and normally limits the change to L0–L1 unless a clear content defect exists.

## 5. Preservation Score

`preservation_score` is an integer from 0 to 100 representing how much existing value should remain unchanged.

Guidance:
- 80–100: Strong original value or monetization structure; surgical edits only.
- 60–79: Meaningful value exists; preserve most content and layout.
- 40–59: Mixed quality; component-level restructuring is possible.
- 0–39: Little proven value or severe mismatch; broader rewrite may be justified.

Protected elements include advertisements, affiliate links, CTA blocks, product links, original reviews, first-hand experience, comparison tables, original images, custom HTML, conclusions that express the author's tested judgment, and verified high-performing passages.

## 6. Rewrite Level

- `L0`: No content change.
- `L1`: Micro edit; wording, clarity, or one small component. Typical budget 1–10%.
- `L2`: Targeted edit; multiple metadata/structure components without broad body replacement. Typical budget 11–20%.
- `L3`: Section-level rewrite or limited expansion. Typical budget 21–35%.
- `L4`: Broad rewrite, 36% or more. Requires explicit justification and normally manual review.

Production default is L0–L2. L3 requires a documented content gap. L4 is exceptional and must not be selected merely because full text was requested.

## 7. Rewrite Scope

- `S0`: No change.
- `S1`: One component.
- `S2`: Two components.
- `S3`: Three to four components.
- `S4`: Multiple sections including body changes.
- `S5`: Article-wide restructuring or replacement.

Scope counts changed components, not the length of the answer.

## 8. Change Budget

`change_budget_percent` is the maximum estimated share of the existing article that may be altered. It must be set before drafting and validated after drafting.

Default ceilings:
- L0: 0%
- L1: 10%
- L2: 20%
- L3: 35%
- L4: 100%, with justification and risk review

Metadata-only changes do not authorize unrelated body rewriting. When the budget cannot be measured precisely, use a conservative component-based estimate and record the method in `validation.notes`.

## 9. Risk

- `LOW`: Reversible editorial change; no material factual, legal, medical, financial, or monetization risk.
- `MEDIUM`: Meaningful structural change, unverified supporting data, or possible effect on conversion/monetization.
- `HIGH`: Broad rewrite, removal of protected elements, high-stakes claim, unsupported numeric claim, or contract violation. Requires review or block.

## 10. Presentation quality

The human-facing response starts directly with the result. It must include:
- Improvement necessity
- Primary search intent
- Changed components
- Work-time estimate
- Concise improvement summary
- Before / After / Expected effect / Reason for each changed component
- Warnings only when action or review is genuinely required

Do not output unchanged sections merely to create volume. Do not duplicate machine `information` as human confirmation items.

## 11. Release gates

A result is product-quality only when:
- Primary intent is preserved.
- Protected elements are preserved or explicitly approved for change.
- Actual changes stay within the budget.
- Rewrite Level and Scope match the output.
- Title is at most 45 Japanese characters; meta description is at most 140 characters.
- Change flags and new values match the human output.
- No unsupported performance forecast is present.
- JSON validates against the frozen contract.
- No English analysis or internal reasoning leaks into the answer.
