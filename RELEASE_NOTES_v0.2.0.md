# SIMS Writer v0.2.0 Quality Freeze

This release freezes the quality behavior derived from the 10-article real-content regression test.

## Highlights
- Editing-first behavior and preservation-first policy
- Formal `LOW_SAMPLE` and `POSITION_OPPORTUNITY` diagnoses
- Frozen Rewrite Level L0–L4, Rewrite Scope S0–S5, Change Budget, Preservation Score, and risk
- Presentation Template with Before / After / Expected effect / Reason
- Closed SIMS Feedback JSON v2.0 schema
- Validation Layer covering intent, protected elements, budget, scope, flags, claims, language, and contract validity

## Compatibility
The default feedback contract moves from v1.2 to v2.0. Consumers must update field validation. User-provided strict contracts continue to take priority.
