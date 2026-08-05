# SIMS Writer v1.3.6 — Publication Pipeline Lock

Root cause: conflicting Contract 2.0 instruction and permissive legacy-output preservation allowed Claude to skip structured QA evidence.

Fixes:
- Contract 2.1 lock.
- Mandatory structured Publication QA.
- Initial/final verdict and review trace in feedback.
- Four operational failure patterns added to the release gate.
- Compatibility maintained for existing Runtime status fields.
