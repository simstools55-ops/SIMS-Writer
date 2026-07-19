# Migration Guide v0.2.3

1. Replace the repository contents with this complete ZIP.
2. Replace the Claude Project files with `SIMS-Writer-Claude-v0.2.3-Validation-Hotfix.zip`.
3. Do not retain the v0.2.2 validation instruction file as a competing source.
4. Run `pytest tests/validation-hotfix-v0.2.3 -q`.
5. Re-run one smoke article containing a named person or uncommon language claim.
