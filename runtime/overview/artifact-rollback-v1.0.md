# Artifact Rollback v1.0

SIMS Writer can restore a previously archived publication artifact set from `.history/<execution_id>/`.

The rollback operation validates that all tracked files exist, archives the currently active execution, restores the selected execution, reruns publication artifact validation, updates `execution-history.json`, and writes `rollback-manifest.json`.

CLI example:

```bash
python -m runtime.sims_writer_runtime.cli \
  --output ./output \
  --rollback-execution-id <execution_id>
```

A rollback is rejected when the history file is missing, the execution is unknown, or the archive is incomplete. The operation never fabricates missing files.
