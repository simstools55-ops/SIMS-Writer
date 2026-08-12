# Evidence Contamination QA v2.0

This QA runs after per-change editorial classification and before user-output serialization.

1. Collect every material claim whose evidence level is LOW or NONE.
2. Scan every proposed `PUBLIC_OK` change for those claims or their normalized claim IDs.
3. If found, reclassify the contaminated change:
   - LOW evidence -> Writer repairs/researches; if still LOW, `INTERNAL_REJECT`;
   - NONE or contradicted evidence -> `INTERNAL_REJECT`.
4. Record `EVIDENCE-CONTAMINATION-001` in the internal audit trace.
5. Do not solve the contradiction by hiding the warning while leaving the claim in public copy.

Canonical example: a monthly upload limit is unverified and proposed as USER_DECISION, but the same limit appears in a PUBLIC_OK introduction. The introduction must not remain PUBLIC_OK.
