# v1 Compatibility Specification

- `format: SIMS_FEEDBACK_V1` は `SIMS_FEEDBACK` に正規化する。
- `version: 1.0|1.1|1.2` は `2.1` に変換する。
- v1の原値は `legacy` に保持する。
- v2.1必須値が導出不能なら `manual_review_required` とする。
- 互換変換時は `LEGACY_FIELD_MAPPED` をwarning codesへ追加する。
