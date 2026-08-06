# SIMS Writer Shared Knowledge Mapping v1.1.0

| 共通知識 | Writerでの適用 |
|---|---|
| Intent Gap | 導入・見出し・FAQ・結論の局所改善根拠 |
| Hidden Anxiety | 未回答かつ判断影響がある場合のみ追加 |
| Evidence Transparency | 断定度、警告、要確認事項へ反映 |
| SERP Entity Preservation | タイトル・メタ・導入の保護監査 |
| Internal Link Semantics | 候補の採用・保留・不採用判定 |
| FAQ Evolution | 本文読後の残存疑問だけを追加・改訂・統合・削除 |
| Conditional Editorial Opinion | 根拠があり既存判断支援が不足する場合だけ条件付き結論を提示 |
| Decision Support | 既存の判断支援が不足するときだけ提案 |

Preservation Score、Rewrite Level、Rewrite Scope、Change Budgetを上書きしない。


## v1.2.0 Platform and Quality application boundary

- Shared Editorial Knowledge remains the source of truth for product-neutral editorial knowledge.
- SIMS Writer applies that knowledge through `product/quality/QUALITY_FRAMEWORK.md`.
- Platform-specific formatting and CMS constraints are governed by `product/platform/SIMS_PLATFORM_GUIDE.md` in the Writer repository.
- Writer Quality Gates, publication formatting, Before/After presentation, and Claude output constraints are not promoted to Shared Knowledge.
- Claude Project consumes the same Writer guides and the verified read-only Shared snapshot.


## v1.2.0 Search Console Query Data application

- `query-data-analysis.md`を最大200件の生クエリ解析へ適用する。
- Coverageは分析信頼度の調整に使い、診断コードを独自追加しない。
- Writerは元クエリを保持し、内部正規化・クラスタリング結果と区別する。
- QUERY MIX、CONTENT GAP、別記事候補、カニバリ候補はEvidence Boundaryを守る。


## Shared v1.3.0 Common Validation Mapping

- VAL-FACT-001 数値整合性
- VAL-EVIDENCE-002 Evidence境界
- VAL-CAUSAL-001 因果表現
- VAL-CONSISTENCY-001 論理整合性
- VAL-ENTITY-001 HTML Entity整合性
- VAL-LINK-001 内部リンク整合性


## v2.0 Editorial application

`editorial-decision-and-visibility.md`、`COPY_READY_OUTPUT_STANDARD_V2.md`、`PUBLICATION_VISIBILITY_POLICY_V2.md`をWriterのEditorial Decision Layerと利用者向け出力生成に適用する。


## v2.0.0 RC1 Four-Layer Architecture
Knowledge / Strategy / Evidence / Patternを分離し、修正前にEditorial Strategyを確定します。


## v2.1.0 Quality Pattern Library

Writerは `quality/QUALITY_PATTERN_LIBRARY.md` を運用試験Learningの正本として必須参照する。
新しい指摘は ARTICLE_SPECIFIC / PATTERN_CANDIDATE / MAPPING_DEFECT / VALIDATION_DEFECT / PREFERENCE_ONLY に分類し、同一問題の再発時は個別文言修正ではなくMappingまたはValidationを修正する。


## v2.2.0 Learning Registry

Writerは `learning/LEARNING_REGISTRY.json` と `learning/LEARNING_SPRINT_PLAYBOOK.md` を実記事試験Learningの追跡正本として参照する。
Writer回答の評価では修正提案より先に5分類を確定し、ARTICLE_SPECIFICとPREFERENCE_ONLYだけでは製品版を更新しない。
MAPPING_DEFECTとVALIDATION_DEFECTには回帰fixtureを必須とする。

## Publication Integrity v2.3

Writerは以下をRuntimeの最終公開ゲートへ適用する。

- `knowledge/publication-integrity-and-dynamic-information.md`
- `knowledge/affiliate-cta-boundary.md`
- `knowledge/faq-publication-consistency.md`
- `quality/PUBLICATION_INTEGRITY_STANDARD_V2_3.md`
- `validation/publication-integrity-validation.md`
- `patterns/dynamic-claim-safe-rewrite-pattern.md`

## v2.4 Real-article validation mapping

Writerは最終出力前に `validation/real-article-publication-validation.md` を必須適用する。Search Console需要と事実根拠を分離し、LOW_SAMPLE、Winner Query、YMYL、内部リンク、タイトル約束を新規v2.4正本へ接続する。実記事8事例はLearning Registryと回帰fixtureで追跡する。

## v3.0 Temporal and architecture mapping

Writer must load `KS-SHARED-TEMPORAL` when date-sensitive, event-based, deadline, planned, active, completed, or expired claims are present. It applies Lifecycle Detection before editing-plan generation, uses contradiction and preservation audits, and exposes only supported optional machine fields. `CONTENT_STALE`, `TEMPORAL_SHIFT`, `LIFECYCLE_CHANGE`, `CONTENT_EXPIRED`, and `CONTRADICTION_DETECTED` are validation/diagnostic signals, not automatic full-rewrite orders.

## Revenue First Validation v3.1.0

Writer must load `product/revenue-first-validation-principle.md` and `validation/revenue-first-validation.md` before final publication classification. `patterns/intent-drift-cross-link-pattern.md` remains a PATTERN_CANDIDATE until a second independent real-article confirmation.
