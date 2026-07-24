# Final Output Integration Instructions v1.3.6

This file is a mandatory final gate and overrides older output examples.

1. Run Self QA before rendering any user-visible publication candidate.
2. Render only the final reviewed draft.
3. Require a canonical `publication_qa` object with initial and final verdicts plus `review_trace`.
4. Do not treat a standalone `qa_verdict` or prose `PASS` declaration as proof of QA execution.
5. For `PASS_WITH_MINOR_FIX`, expose only the corrected After text and record the fix.
6. For `PASS_WITH_REQUIRED_FIX` or `FAIL`, set `publishable: false`; do not call the draft publishable.
7. Canonicalize Contract 2.1 before output: no empty strings, no unchanged entries in `changes[]`, no duplicate boolean/status fields, and no legacy `version`, `change_flags`, or `diagnosis_code`.
8. Every changed item has `target`, `implementation_status`, `before`, `after`, and `reason`.
9. Validate Winner Query preservation, evidence strength, numeric consistency, HTML entities, internal-link state, and JSON completeness immediately before final rendering.
