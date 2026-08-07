# SIMS Writer 3.3.1-RC3

## Doctor Referral Output Contract Gate

Real-article regression A000043 exposed a contract regression: Writer respected the Doctor treatment scope and produced correct Before/After edits, but returned legacy `SIMS_FEEDBACK_V2`, which SBM correctly rejected because the request required `SIMS_WRITER_TREATMENT_RESULT_V1`.

### Fix
- Added request-aware output contract routing.
- `return_contract` is authoritative.
- `SIMS_WRITER_TREATMENT_REQUEST_V1` / `DOCTOR_REFERRAL_TREATMENT` always returns `SIMS_WRITER_TREATMENT_RESULT_V1` Contract 1.0.
- Standard Writer improvement remains `SIMS_FEEDBACK_V2` Contract 4.2.
- Added a final Contract Gate and A000043 regression coverage.

Shared 3.5.0 already contains the canonical treatment contracts/adapters; no Shared version bump is required.
