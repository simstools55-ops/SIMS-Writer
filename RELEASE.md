# SIMS Writer Repository v1.10.0

Status: Quality UAT Preview

This release adds real-article Claude Project UAT evidence capture and a conservative machine-readable readiness gate. It does not declare general user testing ready without recorded evidence.

## Release gate

Run:

```bash
python tools/test_repository.py
```

## User-test readiness evaluation

```bash
python -m runtime.sims_writer_runtime.cli \
  --evaluate-user-test-readiness ./uat-evidence \
  --output ./uat-report
```
