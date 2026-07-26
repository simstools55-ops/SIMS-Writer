# Editorial Planner v2.2

The planner receives the SERP evidence gate result, SERP analysis, intent model, gap analysis, preservation audit and evidence audit before selecting edits.

## Progressive precondition
When average position is greater than 3.0:
1. Run the SERP Evidence Gate.
2. `verified`: continue full planning.
3. `partial`: run Progressive Editing Engine for every component. Do not stop the whole article.
4. `unavailable`: permit only non-SERP mechanical or authoritative factual corrections.
5. Never use Search Console query rows alone to authorize content expansion.

In partial mode, title, meta and introduction may progress when they accurately summarize supported existing content and do not add an unverified search promise. Headings, FAQ, body and structure require component-level gap support and normally become USER_DECISION until coverage is verified.

Search Console query rows may identify investigation candidates, but they cannot alone authorize content expansion.

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


## Evidence Layer lock (v2.0.0-rc.1)
Before planning any content addition, combine Search Console signals, verified SERP findings, and claim-level evidence. `SUPPORTED_GAP` may enter normal planning; `DECISION_GAP` may produce only USER_DECISION; `UNSUPPORTED_GAP` must become INTERNAL_REJECT. A low-evidence claim cannot be inserted into another PUBLIC_OK component.


## Progressive Editing lock (v2.0.0-rc.1)
A blocked component must not block unrelated safe edits. Apply SERP status, evidence level and change basis per component, then send only completed PUBLIC_OK and actionable USER_DECISION items to output.
