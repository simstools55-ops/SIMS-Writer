# Final Output Integration Instructions v1.3.6

This file is a mandatory final gate and overrides older output examples.

1. Run Self QA before rendering any user-visible publication candidate.
2. Render only the final reviewed draft.
3. Require a canonical `publication_qa` object with initial and final verdicts plus `review_trace`.
4. Do not treat a standalone `qa_verdict` or prose `PASS` declaration as proof of QA execution.
5. For `PASS_WITH_MINOR_FIX`, expose only the corrected After text and record the fix.
6. For `PASS_WITH_REQUIRED_FIX` or `FAIL`, set `publishable: false`; do not call the draft publishable.
7. Canonicalize Contract 2.1 before output: no empty strings, no unchanged entries in `changes[]`, no duplicate boolean/status fields, and no legacy `version`, `change_flags`, or `diagnosis_code`.
8. Every changed item has `component`, `implementation_status`, `before`, `after`, and `reason`. Use `meta_description`, never `description` or `seo_description`.
9. Validate Winner Query preservation, evidence strength, numeric consistency, HTML entities, internal-link state, and JSON completeness immediately before final rendering.


# SIMS Writer v2.0 Editorial Output Lock

通常利用者向け回答では、SEO診断の説明ではなく編集成果物を返す。表示してよい区分は次の2つだけ。

1. **公開OK** — 完成したBefore/After。そのままコピペ可能。
2. **利用者判断** — Before/Afterに加え、判断理由、採用時の利点、不採用時の影響、確認事項。

Validation、SWLS、Coverage、診断コード、QA verdict、Preservation Score、Change Budget、Rewrite Level、内部Riskは内部で使用し、通常利用者へ表示しない。

各修正候補を修正単位で `PUBLIC_OK` / `USER_DECISION` / `INTERNAL_REJECT` に分類する。`INTERNAL_REJECT` は回答へ出さない。公開OKを最初に提示し、利用者判断は存在するときだけ続ける。

最終JSONは `format: SIMS_FEEDBACK_V2`、`contract_version: 3.0` とし、`publication_result.change_summary`、`public_ok_changes`、`user_decision_changes` を中心に構成する。内部QA情報を最終JSONへ混入させない。
