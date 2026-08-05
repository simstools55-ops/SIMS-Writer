# SIMS Shared Editorial Knowledge v3.2.0

## SBM-centered Platform Contract

This release establishes SIMS-Blog-Manager as the workflow orchestrator and system of record for the minimum diagnosis-treatment loop.

### Added

- SBM-issued CaseID and canonical Case lifecycle
- Doctor-to-SBM Case Result V2
- SBM-to-Writer Treatment Request V1
- Writer-to-SBM Treatment Result V1
- Workflow Lock and state-ownership rules
- Re-examination routing through SBM

### Changed

- Doctor now recommends treatment through a Referral returned to SBM.
- Specialist products return official results to SBM.
- Direct Doctor-to-Writer routing is deprecated.

### Compatibility

Legacy V1 Doctor-centered contracts remain documented for adapters. Existing SBM-to-Writer normal improvement workflows are unaffected.
