## 2.0.0-rc.3

- 公開可否の冒頭一文を必須化。
- 公開OK理由を平易な一文以内へ短文化。
- 内部リンク全件不採用時の表示を一文へ固定。
- UX Filterを最終出力ゲートへ追加。

# 2.0.0-rc.1

- Editorial Strategy Engine
- Four-layer Shared architecture
- Contract 4.0 minimal delivery

# 2.0.0-rc.1

- Added Knowledge Confidence and Freshness gates.

## 2.0.0-rc.1

# v2.0.0-rc.1 — Progressive Editing Engine

- Added component-scoped SERP and Evidence decisions.
- Partial SERP inspection now permits safe title, meta and introduction work while uncertain content expansion is held or sent to user decision.
- Preserved Evidence contamination QA and silent internal rejection.
- Simplified internal-link user output.

## 2.0.0-rc.1

# v2.0.0-rc.1 — Integrated Evidence Layer

- Search Console・verified SERP・一次/二次情報を統合するEvidence Layerを追加。
- HIGH/MEDIUM/LOW/NONEの内部Evidence判定をEditorial Decisionへ接続。
- LOWはUSER_DECISION、NONEはINTERNAL_REJECTへ固定。
- 未確認事実がPUBLIC_OKの別コンポーネントへ混入する矛盾をEVIDENCE-CONTAMINATION-001で遮断。
- GapをSUPPORTED_GAP / DECISION_GAP / UNSUPPORTED_GAP / NO_GAP / SEPARATE_INTENTへ分類。
- 利用者向けには内部スコアを出さず、必要な確認資料だけを提示。
- 冒頭に一行の平易な改善戦略を表示可能にした。

## 2.0.0-dev.3

- SERP未確認を警告ではなく編集停止条件へ変更。
- 順位3位以下では、見出し・FAQ・本文・構成・タイトル訴求変更にverified SERPを必須化。
- Search Consoleクエリだけを根拠とした内容追加を禁止。
- SERP未確認時の許可修正を機械的・独立検証済み修正へ限定。
- SERP未確認とSERP依存編集の同時出力をPublication QAで拒否。
- 内部リンク不採用一覧などの利用者表示を簡略化。

# Changelog

## 2.0.0-dev.2
- Added mandatory SERP-first intent and gap analysis for main-query positions below the top three.
- Added non-fabrication and unavailable-SERP safeguards.


## 2.0.0-dev.1

- Introduced user-centered SEO editorial output architecture.
- Added PUBLIC_OK / USER_DECISION / INTERNAL_REJECT separation.
- Moved QA and validation detail to internal audit records.

# v1.4.0
- Validationメッセージを簡潔化し監査形式を統一
- review_traceをchecked配列中心へ構造化
- cycle数とauto_fixesの正規化を強化

# v1.3.9

- Validation Message Integrity Hotfix。空メッセージを正例・Schema・Normalizer・最終ゲート・テストの全層で禁止。

## 1.3.8 - Regression Hotfix

# SIMS Writer Claude v1.3.8 Regression Hotfix

旧出力指示との競合を除去し、Canonical Contract、日本語表示、Reviewer停止条件を最終強制しました。

# 1.3.7

# SIMS Writer v1.3.7 — Contract Cleanup, Reviewer Precision, Japanese UX and Release Cleaner

- `changes[].target`を`component`へ統一
- 空文字と未変更項目の出力を抑止
- `auto_fixes`、`review_trace`、QA契約識別子を固定
- 内部リンク評価を候補単位で保持
- LOW/MEDIUM Coverage時の断定抑制を強化
- 利用者向け専門用語を日本語基本・初出のみ英語併記へ変更
- `.pytest_cache`、`__pycache__`等を除去するRelease Cleanerを追加

# 1.3.6
- Locked Publication QA pipeline and canonical final output.

# 1.3.0 - Quality & Validation Hardening

- Writer本体v1.3.0と完全同期
- Shared Snapshot v1.3.0
- Contract 2.1運用指示を追加


## 1.1.1 - 2026-07-22
- Shared Editorial Knowledge v1.1.1へ同期。
- 中心主張優先検証、Source-Scope表現、LOW_SAMPLE時の最小変更を強化。
- 内部リンクのadopted / pending / rejected判定を明確化。

## 1.1.0 - 2026-07-21
- Production baseline.

## 1.3.2 - Publication QA Foundation

- Added mandatory final Publication QA workflow and safe auto-fix boundaries.
- Added five-level publication verdicts and release gate documentation.

## 1.3.3 - Regression Evaluation Profiles

- Added formal Publication QA evaluation standard.
- Added five Official Regression Suite case profiles and expected findings.
- Added regression readiness runner and QA checklist integration.
- Source article fixtures remain pending and are reported as SKIP.

## 1.3.4
- Added Self QA runtime instructions and platform-neutral QA contract reference.

## 1.3.5
- Added QA-reviewed final output integration rules.

## 2.0.0-rc.3
- Stabilized final output integration and removed active legacy contract conflicts.
