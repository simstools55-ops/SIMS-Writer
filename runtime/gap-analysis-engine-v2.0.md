# Gap Analysis Engine v2.0

Compare the intent model and top-result evidence with the target article.

Classify each observation as:
- `covered_strongly`: present, correct and easy to find;
- `covered_weakly`: present but unclear, buried or incomplete;
- `missing_material`: absent and necessary to satisfy the intent;
- `competitor_common_nonessential`: common in results but not necessary;
- `article_unique_value`: useful original value that must be preserved;
- `accuracy_or_freshness_risk`: needs authoritative verification;
- `separate_article_boundary`: a distinct intent better handled elsewhere.

A missing item becomes an edit candidate only when it is both intent-material and supportable by evidence. Competitor frequency alone is never sufficient.
