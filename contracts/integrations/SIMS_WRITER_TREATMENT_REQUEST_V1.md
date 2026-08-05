# SIMS Writer Doctor Referral Treatment Contract v1.0

## Canonical route

`SIMS-Blog-Manager -> SIMS Writer -> SIMS-Blog-Manager`

Writer must not return the treatment result directly to Doctor. SBM owns the CaseID,
workflow state, publication decision, measurement, and reexamination request.

## Input

- `format`: `SIMS_WRITER_TREATMENT_REQUEST_V1`
- `request_mode`: `DOCTOR_REFERRAL_TREATMENT`
- `case_id`: generated and owned by SBM
- `doctor_referral.allowed_scope`: the only components Writer may edit
- `doctor_referral.blocked_scope`: components Writer must not edit
- `workflow.treatment_allowed`: must be `true`

## Runtime rules

1. Do not repeat the Doctor diagnosis.
2. Edit only components listed in `allowed_scope`.
3. Do not edit anything listed in `blocked_scope`.
4. Report additional findings without silently fixing them.
5. Preserve the CaseID and ArticleID.
6. Return `SIMS_WRITER_TREATMENT_RESULT_V1` to SBM.

## Backward compatibility

`SIMS_DOCTOR_WRITER_REQUEST_V1` remains accepted through the legacy adapter, but
is deprecated for new platform workflows.
