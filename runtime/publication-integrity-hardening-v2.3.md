# Publication Integrity Hardening Runtime v2.3

## Stage order

After editorial changes are drafted and before final packaging:

1. Dynamic Information Audit
2. Official Source/Freshness Audit
3. Marketing Claim Sweep
4. Affiliate CTA Sweep
5. FAQ Consistency Audit
6. Cross-component Claim Sweep
7. Publication Text Freeze
8. Contract 4.2 JSON generation
9. Text/JSON Synchronization Audit

## Dynamic claim detection

Search the entire article and proposed changes for price, discount, shipping, stock, campaign, guarantee, app/OS feature, setting path, UI, limit, plan, period, frequency and non-existence claims.

Existing article text is not evidence of freshness. Any reused dynamic claim must be revalidated.

## CTA boundary

Preserve URL, affiliate code, tracking parameters and embedded ad code. Treat surrounding CTA wording as editable and high-priority validation content.

## Cross-component sweep

When a claim is removed or qualified, repeat a semantic and literal sweep across title, meta, introduction, headings, body, FAQ, conclusion, CTA and JSON. A stale duplicate blocks PUBLIC_OK.

## Synchronization

Generate JSON only after publication text is frozen. Compare every public_ok_changes/user_decision_changes `after` value and change_summary with the final displayed text. Any mismatch is FAIL.
