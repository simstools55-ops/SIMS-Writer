# SIMS Writer Repository v1.1.0

## Status

Product 1.0 post-release implementation.

## Implemented Vertical Slice

- Multiple improvement request batch processing
- Isolated per-article artifact directories
- Continue-on-error processing and explicit error artifacts
- Batch JSON and Markdown summaries
- Existing single-article publication lifecycle retained

## Batch Command

```bash
python -m runtime.sims_writer_runtime.cli \
  --batch-input examples/batch/requests \
  --output batch-output
```

## Release Gate

```bash
python tools/test_repository.py
```

The repository ZIP must pass the same gate after re-extraction.
