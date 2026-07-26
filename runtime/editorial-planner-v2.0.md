# Editorial Planner v2.1

The planner receives the SERP evidence gate result, SERP analysis, intent model, gap analysis, preservation audit and evidence audit before selecting edits.

## Blocking precondition
When average position is greater than 3.0:
1. Run the SERP Evidence Gate.
2. If the gate is `OPEN`, continue with the full planning order.
3. If the gate is `LIMITED`, plan only whitelist corrections that do not depend on current search intent or competitor gaps.
4. If a proposed heading, FAQ, body, structure or title-promise change depends on SERP comparison while the gate is not `OPEN`, classify it as `INTERNAL_REJECT`; do not present it as 公開OK or 利用者判断.

Search Console query rows may identify questions worth investigating, but they cannot alone authorize content expansion when the mandatory SERP inspection is incomplete.

## Planning order after gate opens
1. Preserve article-unique value and proven winner entities.
2. Correct factual, promise or consistency defects.
3. Strengthen weakly covered material.
4. Add only material missing information.
5. Remove or relocate off-intent material when safe.
6. Align title, meta and introduction with the final edited content.

Every proposed change must contain an internal `change_basis`:
- `search_intent`;
- `serp_gap`;
- `accuracy`;
- `consistency`;
- `usability`;
- `preservation`;
- `mechanical`.

No change may be proposed merely because it appears in a competitor article.


## Evidence Layer lock (v2.0.0-dev.4)
Before planning any content addition, combine Search Console signals, verified SERP findings, and claim-level evidence. `SUPPORTED_GAP` may enter normal planning; `DECISION_GAP` may produce only USER_DECISION; `UNSUPPORTED_GAP` must become INTERNAL_REJECT. A low-evidence claim cannot be inserted into another PUBLIC_OK component.
