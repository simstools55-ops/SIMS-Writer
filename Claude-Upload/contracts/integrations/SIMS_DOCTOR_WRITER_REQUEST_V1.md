# SIMS_DOCTOR_WRITER_REQUEST_V1

Writer v3.1.1 accepts a Doctor envelope only through a dedicated adapter.
The adapter maps the request to the existing Writer internal request model.
The editorial pipeline, publication policy, and `SIMS_FEEDBACK_V2` remain unchanged.

Required correlation: `site_id`, `case_id`, `treatment_id`, `article_id`, `message_id`.
