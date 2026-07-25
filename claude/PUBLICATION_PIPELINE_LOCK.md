## v1.3.6 Mandatory Publication Pipeline Lock

This section overrides every older output example or template in the repository.

1. Build the improvement draft internally; do not present it yet.
2. Run Publication QA against the draft and draft feedback.
3. Apply only safe local fixes permitted by `AUTO_FIX_RULES.md`.
4. Re-run the same QA after every fix, up to two cycles.
5. Present only the final QA-reviewed Before/After. Never present a rejected pre-fix draft as the publication candidate.
6. The final JSON must contain `format: "SIMS_FEEDBACK_V2"`, `contract_version: "2.1"`, canonical `changes[]`, `validation`, and `publication_qa`.
7. `publication_qa` must contain `contract`, `initial_verdict`, `final_verdict`, `publishable`, `release_action`, `auto_fixes`, `review_cycles_used`, `review_trace`, and `unresolved_findings`. `auto_fixes`, `review_trace`, and `unresolved_findings` are structured arrays. Do not emit `auto_fix_applied`.
8. A written claim such as「QA済み」「PASS」is invalid unless the corresponding `publication_qa` object is present and internally consistent.
9. Do not output a separate `qa_verdict` field as a substitute for `publication_qa`.
10. Do not use empty strings. Do not place unchanged components in `changes[]`; record them under `protected_elements` or `preserved_components`.
11. Each changed component must include `component`, `implementation_status`, `before`, `after`, and `reason`. Use `meta_description`, never `description` or `seo_description`.
12. Before `PASS`, explicitly check Winner Query preservation, unsupported causal/generalized claims, numeric consistency, HTML entities, internal-link implementation state, and Contract completeness.
13. If required findings remain, set `final_verdict` to `PASS_WITH_REQUIRED_FIX` or `FAIL`, set `publishable` to false, and do not label the draft publishable.
