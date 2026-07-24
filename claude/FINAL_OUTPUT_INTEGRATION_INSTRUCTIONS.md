# Final Output Integration Instructions

After Self QA completes:

1. Show the publication verdict first.
2. Use only the final QA-reviewed Before/After content as the publication candidate.
3. When the verdict is `PASS_WITH_MINOR_FIX`, state that the correction has already been applied.
4. When the verdict is `PASS_WITH_REQUIRED_FIX` or `FAIL`, do not label any text as publishable.
5. Preserve the existing `SIMS_FEEDBACK_V2` fields and append QA metadata without renaming legacy fields.
6. Do not expose rejected or pre-fix text inside the machine publication package.
