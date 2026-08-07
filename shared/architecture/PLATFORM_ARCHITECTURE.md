# SIMS Editorial Platform v1.0 Architecture

## Decision

SBM is the Control Plane, workflow orchestrator, and system of record. Doctor, Writer, Creator, and Merge are specialist execution products. Shared Editorial Knowledge is the Knowledge and Contract Plane.

```text
SBM -> Doctor -> SBM -> Writer / Creator / Merge -> SBM -> publication -> monitoring -> re-examination
```

## Product responsibilities

| Product | Canonical responsibility |
|---|---|
| SBM | Identity, Case state, routing, publication records, monitoring, audit |
| Doctor | Diagnosis, cause hypotheses, treatment plan, referral |
| Writer | Existing-article treatment |
| Creator | New-article creation and intent separation |
| Merge | Multi-article consolidation, role separation, redirect/noindex/delete planning |
| Shared | Contracts, enums, common knowledge, validation, governance |

Only SBM changes authoritative Case state. Specialist products report results and recommended next state.
