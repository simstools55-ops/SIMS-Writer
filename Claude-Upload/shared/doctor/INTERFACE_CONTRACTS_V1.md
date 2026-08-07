# SIMS Doctor Interface Contract Registry v0.1.0

> **Deprecated compatibility document.**
>
> This registry describes the former Doctor-centered routing model. The canonical platform contract is now `INTERFACE_CONTRACTS_V2.md`, where SBM issues CaseID, routes all requests, receives all results, and owns workflow state.

## Legacy contracts

| Contract | Source | Target | Responsibility |
|---|---|---|---|
| SIMS_DOCTOR_ARTICLE_CATALOG_V1 | SIMS_BLOG_MANAGER | SIMS_DOCTOR | Article catalog and operational state |
| SIMS_DOCTOR_LONG_TERM_SNAPSHOT_V1 | SIMS_DOCTOR_COLLECTOR | SIMS_DOCTOR_DIAGNOSIS_ENGINE | Long-term aggregate and data quality |
| SIMS_DOCTOR_CASE_DIAGNOSIS_V1 | SIMS_DOCTOR | SIMS_BLOG_MANAGER | Legacy diagnosis Case and lock request |
| SIMS_DOCTOR_WRITER_REQUEST_V1 | SIMS_DOCTOR | SIMS_WRITER | Legacy direct Writer Treatment request |
| SIMS_TREATMENT_RESULT_V1 | Specialist system | SIMS_DOCTOR | Legacy direct Treatment result |
| SIMS_DOCTOR_CASE_RESULT_V1 | SIMS_DOCTOR | SIMS_BLOG_MANAGER | Legacy aggregated Case result |

## Legacy rules retained only for adapters

- `site_id` and `article_id` remain SBM-owned.
- Legacy Doctor-issued `case_id` and direct Doctor/Writer routing may be read by compatibility adapters.
- New implementations must not prefer or newly emit the legacy direct-routing path.
- Unknown optional fields remain ignorable; unknown enum values must not be silently converted.
