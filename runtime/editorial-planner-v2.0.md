# Editorial Planner v2.0

The planner receives the SERP analysis, intent model, gap analysis, preservation audit and evidence audit before selecting edits.

## Planning order
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
- `preservation`.

No change may be proposed merely because it appears in a competitor article.
