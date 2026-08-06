# Platform Treatment Integration

SIMS WriterはSBMからのみTreatment Requestを受信し、SBMへTreatment Resultを返します。
DoctorからWriterへの直接依頼は廃止されています。

## 標準入力

`SIMS_WRITER_TREATMENT_REQUEST_V1`

Writerは`case_id`、`treatment_request_id`、`allowed_scope`、`blocked_scope`、`preservation_targets`を保持します。

## 標準出力

`SIMS_WRITER_TREATMENT_RESULT_V1`

出力にはReferral Compliance、公開OK変更、利用者判断変更、Preservation Report、Publication Readiness、Follow-up Referral候補を含めます。

## Legacy

従来の`SIMS_FEEDBACK_V2`は継続サポートし、SBM AdapterでPlatform Resultへ正規化します。
