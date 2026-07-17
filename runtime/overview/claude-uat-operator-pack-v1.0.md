# Claude UAT Operator Pack v1.0

Prepared UAT sessions can be converted into a guided operator pack without modifying evidence.

```bash
python -m runtime.sims_writer_runtime.cli \
  --build-claude-uat-operator-pack ./uat-sessions/UAT-ID \
  --output ./uat-operator
```

The generated pack contains one prompt sheet per article, a scoring guide, a progress checklist, and a machine-readable manifest. It is an execution aid only; readiness remains based on measured session evidence.
