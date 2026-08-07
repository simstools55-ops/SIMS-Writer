# SIMS_FEEDBACK_V2 Adapter

SBM continues to accept `SIMS_FEEDBACK_V2` contract versions 2.1, 3.0, and 4.2. The adapter maps article identity, changes, publication_result, completed_at, and recommended_review_days into `SIMS_WRITER_TREATMENT_RESULT_V1`. `changes` remains optional when a valid publication_result is present. Legacy input is accepted; new Platform routing should prefer the v1 treatment result.
