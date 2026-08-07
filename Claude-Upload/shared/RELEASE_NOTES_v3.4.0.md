# SIMS Shared Editorial Knowledge v3.4.0

Date: 2026-08-07

## Added

- Platform boundary for Google Algorithm / Search update evidence.
- Integrated Evidence Policy linking source confidence, freshness, contradiction, and multi-source diagnostic judgement.
- Platform-visible Treatment Strategy vocabulary: WAIT / LIGHT_FIX / NORMAL_REWRITE / FULL_REWRITE.
- Additive Doctor interface guidance for Algorithm Impact Assessment, WAIT plans, user ToDo, and evidence-based guidance.

## Architecture

- Preserves `SBM -> Doctor -> SBM -> Writer / Creator / Merge -> SBM`.
- Algorithm information is Evidence, not Diagnosis.
- Doctor-specific scoring and causation logic remain outside Shared.
- Existing Evidence Confidence documents remain canonical; no duplicate confidence framework was introduced.

## Compatibility

This is a backward-compatible Shared minor release for SIMS Editorial Platform 1.x.
