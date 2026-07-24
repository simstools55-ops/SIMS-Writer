# Final Publication Output v1.0

The Runtime must generate user-visible output only from the final QA-reviewed draft.

## Rules
1. `PASS`, `PASS_WITH_WARNING`, and `PASS_WITH_MINOR_FIX` may expose publication content.
2. `PASS_WITH_REQUIRED_FIX` and `FAIL` must set publication content to null and retain the draft only as `held_draft`.
3. QA Before/After details belong to `publication_view`; the machine publication package exposes only changed component names so rejected text cannot leak into release content.
4. Existing SIMS_FEEDBACK fields remain unchanged. QA metadata is appended under `publication_qa`.
