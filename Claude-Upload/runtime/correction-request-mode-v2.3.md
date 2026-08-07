# Correction Request Mode v2.3

## Trigger

A message beginning with `CORRECTION_REQUEST` after a Writer output activates local correction mode.

## Rules

- Use the immediately preceding answer as the baseline.
- Modify only the named targets and dependent JSON fields.
- Do not rerun SERP analysis or redesign unrelated title, meta, structure or internal links unless explicitly requested.
- Preserve site/article identity, measurement settings and unchanged Before/After entries.
- Re-run publication integrity validation for the corrected claim across all components.
- Output corrected full reusable text and one complete Contract 4.2 JSON block.
- Update `after`, `reason`, `change_summary` and `new_values` only where the correction changes them.
- Never ask the user to hand-edit JSON.

## Failure

If the named correction reveals the same unsupported claim elsewhere, correct all occurrences and explicitly state the dependent scope. Do not silently retain contradictory wording.
