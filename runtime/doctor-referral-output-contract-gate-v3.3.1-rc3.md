# Doctor Referral Output Contract Gate v3.3.1-RC3

## Purpose
Prevent a Doctor Referral treatment from accidentally returning the legacy `SIMS_FEEDBACK_V2` machine result.

## Routing rule
The final machine JSON contract is resolved in this order:

1. `return_contract.format` in the SBM request is authoritative.
2. If input `format == SIMS_WRITER_TREATMENT_REQUEST_V1`, return `SIMS_WRITER_TREATMENT_RESULT_V1` Contract 1.0.
3. If `request_mode == DOCTOR_REFERRAL_TREATMENT`, return `SIMS_WRITER_TREATMENT_RESULT_V1` Contract 1.0.
4. Otherwise retain normal Writer output `SIMS_FEEDBACK_V2` Contract 4.2.

## Hard prohibition
When Doctor Referral Treatment is active, `SIMS_FEEDBACK_V2` must not be emitted as the final result JSON. Before final output, compare the expected format with the actual JSON. If they differ, regenerate the machine result before replying.

## Human output
The Human Presentation is unchanged: publication status, what to do, complete Before/After, reason, expected effect, unchanged items, next step, then one machine JSON block at the end.
