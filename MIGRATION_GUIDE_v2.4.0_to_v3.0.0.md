# Migration Guide: Writer v2.4.0 -> v3.0.0

## Compatibility
- Existing user workflow remains unchanged.
- `SIMS_FEEDBACK_V2`, Contract v4.2, and `publication_result` remain authoritative.
- New `analysis_extensions` is optional and additive.
- SBM may ignore unknown fields.

## Repository update
Replace the existing repository contents with the v3.0.0 package. Do not merge old generated manifests. For Claude Project, replace the Writer Claude knowledge files with the v3 package and paste the current project instructions.

## Behavioral changes
- temporal lifecycle review runs for date-sensitive content
- contradictions and preservation signals are audited before editing
- operational learning follows Observation -> Lesson -> Rule -> Pattern -> Knowledge -> Shared
- unresolved material contradictions move to USER_DECISION or block publication readiness
