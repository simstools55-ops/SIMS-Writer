# 3.5.0

- Added Platform-wide Human Experience Architecture and Presentation Framework.
- Added Human/Machine Output policies and Human Usability Gate.
- Declared Creator and Merge in the common Presentation scope without forcing implementation changes in this release.
- Standardized Before/After usability requirements for Writer including Doctor Referral Treatment.

# Changelog

## 3.4.0 - 2026-08-07
- Added Algorithm Evidence platform boundary for Doctor v1.2.
- Added Integrated Evidence Policy without duplicating existing confidence rules.
- Added WAIT / LIGHT_FIX / NORMAL_REWRITE / FULL_REWRITE Treatment Strategy semantics.
- Preserved SBM-mediated specialist routing and kept Doctor-specific algorithm scoring outside Shared.


## 3.3.0 - 2026-08-05

- Added SIMS Editorial Platform v1.0 architecture, workflow, repository governance, Claude operations, and release baseline.
- Added common envelope and canonical v1 schemas for Doctor, Writer, Creator, Merge, publication, monitoring, events, and errors.
- Added common enums, compatibility matrix, Platform manifest, and product-scoped snapshot definitions.
- Added legacy adapters for SIMS_FEEDBACK_V2 and Doctor Case Result V2.
- Added Merge knowledge, safety, preservation, publication-order, and rollback rules.
- Preserved v3.2.0 SBM-centered routing compatibility.

## 3.2.0 - 2026-08-05

- Established SBM as the platform orchestrator and Case lifecycle source of truth.
- Changed CaseID ownership from Doctor to SBM.
- Added `SIMS_DOCTOR_CASE_RESULT_V2`, `SIMS_WRITER_TREATMENT_REQUEST_V1`, and `SIMS_WRITER_TREATMENT_RESULT_V1` to the canonical registry.
- Added the minimum Case lifecycle and Workflow Lock routing rules.
- Deprecated direct Doctor-to-Writer dispatch and Writer-to-Doctor result routing while retaining compatibility documentation.


## v3.1.0 Revenue First Validation

Revenue impact, search intent, winner-query preservation and publication integrity now determine blocking priority. Editorial polish with negligible SEO impact remains non-blocking.
## 3.0.1 - 2026-08-01

- Separated SEO-critical validation from non-blocking quality recommendations.
- Added internal repair and revalidation loop with a three-cycle cap.
- Added publication finalization states and non-blocking follow-up separation.
- Preserved Contract 4.2 compatibility.

# v2.2.0

Operational Learning Registryを追加。実記事試験の知見を分類・追跡し、10記事単位でLearning Sprintを実施します。

# 2.1.0 - Quality Pattern Library

- Operational-test findings are now classified before promotion.
- Added canonical pattern registry and no-loop governance.
- Added mapping and validation requirements for recurring defects.

## 2.0.1 - 2026-07-26

- Hotfix: natural Japanese, publication flag separation, title semantic alignment, terminology consistency.

## 2.0.0 - 2026-07-26

- Released the user-centered SEO editorial system.
- Added final Natural Japanese and similarity-candidate reporting gates.
- Kept Contract 4.2 and all RC2 safety/integration gates unchanged.

## 2.0.0-release-candidate.2 - 2026-07-26

- Added final scope-alignment, device-path variability, and internal-link overlap release gates.
- Prevented title/meta expansion into adjacent intents not covered by the article.
- Required device-specific setting paths to account for OS/version/vendor differences.
- Applied the same cannibalization and role-overlap review to every proposed internal link.

## 2.0.0-release-candidate.1 - 2026-07-26

- Added release final semantic, expectation, YMYL safety and benefit-claim gates.

## 2.0.0-gold.1
- Add quantitative SERP evidence, gap importance, and user-facing decision trace with Contract 4.2.

## 2.0.0-gold.1

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

## 2.0.0-dev.5

# v2.0.0-dev.5 — Progressive Editing Engine

- Added component-scoped SERP and Evidence decisions.
- Partial SERP inspection now permits safe title, meta and introduction work while uncertain content expansion is held or sent to user decision.
- Preserved Evidence contamination QA and silent internal rejection.
- Simplified internal-link user output.

## 2.0.0-dev.5

# v2.0.0-dev.5 — Integrated Evidence Layer

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
- Validation監査メッセージとQA履歴構造を標準化

# v1.3.9

- Validation Message Integrity Hotfix。空メッセージを正例・Schema・Normalizer・最終ゲート・テストの全層で禁止。

## 1.3.8 - Regression Hotfix

# Shared Editorial Knowledge v1.3.8 Regression Hotfix

Canonical Publication QA output, unresolved-finding verdict alignment, claim-precision rules, and Japanese user-facing terminology were hardened.

# 1.3.6
- Locked Publication QA pipeline and canonical final output.

## 1.3.1 - 2026-07-24

- KN-ENTITY-001を明文化し、メタディスクリプションを含むHTML Entity二重エンコード防止規則を強化。
- VAL-ENTITY-001のPASS条件と検出対象を明確化。

# 1.3.0 - Writer Quality & Validation Hardening

- 6つの共通Validationコードを追加
- Writer/Article Creator Mappingへ共通Validationを接続
- 製品固有のQuery IntelligenceとJSON ContractをSharedから分離維持
- Snapshot生成時の版数・Manifest整合性を強化


## 1.2.0 - 2026-07-24
- 最大200件のSearch Console Query Data解析ルールを追加。
- Coverage信頼度、Raw Query Preservation、Intent Action Classificationを追加。
- QUERY MIX、CONTENT GAP、カニバリ判定の推論境界を明文化。

# Changelog

## 1.1.3 - 2026-07-23

### Fixed
- Defined product-scoped Shared snapshots.
- Prohibited cross-product mapping inclusion in Claude packages.
- Removed accidental root-level duplicate and misnamed files that could confuse Project Knowledge.
- Added snapshot boundary validation.

## 1.1.1 - 2026-07-22
- 運用試験Learningを共通知識へ昇格。
- 中心主張優先検証、調査範囲限定表現、Evidence強度別表現を追加。
- Graceful Degradation、既存本文反映、FAQ再構成を正式化。
- Buyer Trust、価格鮮度、Entity Alias、Taxonomy鮮度を追加。

## 1.1.0 - 2026-07-21

- Added FAQ Evolution as shared editorial knowledge.
- Added Conditional Editorial Opinion as shared editorial knowledge.
- Expanded Writer application mapping to all seven validated editorial capabilities.
- Preserved v1.0.0 compatibility and editorial guardrails.

## 1.0.0

- Established the Shared Editorial Knowledge repository and Writer/Article Creator mappings.

## 1.3.2

- Added common Publication QA principles and validation requirements for final editorial release review.

## 1.3.3 - Regression Evaluation Profiles

- Added formal Publication QA evaluation standard.
- Added five Official Regression Suite case profiles and expected findings.
- Added regression readiness runner and QA checklist integration.
- Source article fixtures remain pending and are reported as SKIP.

## 1.3.4
- Added platform-neutral Editorial QA Contract v1.

## 1.3.5
- Added final publication output principles and held-draft suppression rule.

## 2.0.0-gold.1
- Added final integration precedence and visibility validation.

## 2.0.0-gold.1
- Add shared SERP gap explainability pattern.

## 2.3.0

- Added publication integrity and dynamic information standard.
- Added affiliate CTA editable/protected boundary.
- Added FAQ and cross-component consistency validation.
- Added final publication/JSON synchronization requirements.
- Added safe rewrite pattern for unverified dynamic claims.

## 2.4.0 - 2026-07-28

- Added strict real-article Before source integrity and paste-ready After validation.
- Separated Search Console demand from factual evidence.
- Added whole-article supernatural/health and conditional food-safety guards.
- Added LOW_SAMPLE title control, Winner Query protection, title promise alignment and internal-link destination validation.
- Registered eight real-article regression learnings and fixtures.

## 3.0.0 - 2026-08-01
- Added temporal intent and content lifecycle knowledge.
- Added confidence, contradiction, preservation, and learning promotion architecture.
- Added shared registries, policies, recovery pattern, and validation.

## 3.0.2 - 2026-08-01
- Added Fee Subject Clarity and cross-component auto-repair validation.

## 3.1.1
- Added Doctor interface and safety-boundary knowledge.
