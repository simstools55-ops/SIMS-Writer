# Execution History and Diff v1.0

SIMS Writer preserves the previous seven publication artifacts before overwriting an existing output directory. Archived artifacts are stored under `.history/<execution_id>/`.

`execution-history.json` records execution order and superseded state. `artifact-diff.json` compares tracked file checksums and the publication fields `publish_decision`, `seo_title`, `meta_description`, `h1`, and `article_content`.

The initial execution is a baseline and reports `changed: false`. Subsequent executions report changes only against the immediately previous execution.
