# Migration Guide to v0.2.0

1. Replace Claude Project Instructions with `claude/CLAUDE_PROJECT_INSTRUCTIONS.md`.
2. Replace the Claude Knowledge files with the contents of the Quality Freeze Claude package.
3. Update consumers from `SIMS_FEEDBACK_V1` v1.2 to v2.0.
4. Rename any legacy `change_budget` field to `change_budget_percent`.
5. Remove legacy Rewrite Level `L5`; use `L4` with review justification.
6. Treat `diagnosis` as an array.
7. Add `improvement_necessity`, `primary_intent`, `change_flags`, `new_values`, and `validation`.
8. Run repository tests and the Quality Freeze validator before release.
