# SIMS Quality Pattern Library v1.0

## Purpose

運用試験で発見した再発可能な品質問題を、記事固有の修正から切り離して共通ルールへ昇格するための正本です。
同じ指摘を別記事で繰り返さないことを目的とし、SIMS WriterとSIMS Article Creatorは製品別Mappingを通じて適用します。

## Finding Classification Codes

- ARTICLE_SPECIFIC
- PATTERN_CANDIDATE
- MAPPING_DEFECT
- VALIDATION_DEFECT
- PREFERENCE_ONLY

## Promotion Rule

運用試験の指摘は次の順に分類します。

1. 記事固有の事実・語句・URLであるか
2. 他ジャンル・他記事でも再発する可能性があるか
3. 既存Knowledge / Strategy / Evidence / Patternで既に防止できるか
4. 既存ルールで防止できない場合だけ、新規PatternまたはValidationへ昇格する
5. 昇格したルールには回帰テストを必須で紐付ける

## Canonical Pattern Registry

| ID | Pattern | Applies to | Canonical source | Required validation |
|---|---|---|---|---|
| QP-001 | Answer First | title / meta / introduction | `patterns/answer-first-pattern.md` | central answer appears early without unsupported claims |
| QP-002 | SERP Gap Adoption | headings / body / FAQ | `patterns/gap-completion-pattern.md` | Search Console demand + SERP intent + article gap |
| QP-003 | SERP Explainability | user output | `patterns/serp-gap-report-pattern.md` | measured scope only; no invented counts |
| QP-004 | Semantic Title Alignment | article title / SEO title | `patterns/title-semantic-alignment-pattern.md` | number, noun and verb form a true statement |
| QP-005 | Expectation Alignment | title / meta / introduction / body | `patterns/expectation-alignment-pattern.md` | every promise is fulfilled in body |
| QP-006 | Natural Japanese | all user-facing text | `patterns/natural-japanese-pattern.md` | no unnatural noun chains or keyword stuffing |
| QP-007 | Evidence Publication Boundary | factual changes | `patterns/evidence-publication-boundary-pattern.md` | volatile claims require official/primary evidence for PUBLIC_OK |
| QP-008 | YMYL Safety Priority | health / finance / legal / safety | `patterns/ymyl-safety-pattern.md` | safety outranks demand and CTR |
| QP-009 | Internal Link Role Separation | internal links | `patterns/internal-link-role-separation-pattern.md` | reader-next-question fit and overlap/cannibalization review |
| QP-010 | Terminology and Unit Consistency | title / meta / body / FAQ | `patterns/terminology-unit-consistency-pattern.md` | one concept uses one accurate unit and term |
| QP-011 | Scope Alignment | title / meta / headings | `patterns/scope-alignment-pattern.md` | do not expand into adjacent symptoms not handled by body |
| QP-012 | Freshness Qualification | volatile specifications | `patterns/freshness-qualification-pattern.md` | dated facts must be current or explicitly qualified |

## Operational Learning Record

新しい運用試験結果は次の形式で記録します。

- Observation: 発見した問題
- Generalizable rule: 記事を超えて適用できる規則
- Existing canonical rule: 既存ルールで防止できるか
- Action: no change / clarify / add pattern / add validation
- Regression fixture: 再発確認に使う代表ケース
- Product scope: Writer / Creator / Both

## No-Loop Rule

同一カテゴリの指摘が再発した場合、個別記事の文言修正だけで終了してはいけません。

- Canonical ruleが存在しない: Sharedへ昇格する
- Canonical ruleが存在するが未適用: Product MappingまたはRuntime接続を修正する
- Canonical ruleが適用済みだが漏れた: Validationと回帰テストを修正する
- 単なる好み・複数正解: 新規ルールを増やさず、記事固有判断として終了する

## Release Gate

Sharedルールの追加・変更は、次を満たすまで製品リリースへ反映しません。

- Pattern Registry更新
- Writer / Creator Mapping境界確認
- 回帰テスト追加
- Writer用Scoped Snapshot再生成
- 既存ContractとVisibility Policyへの非干渉確認


## Learning Registry Connection (v2.2.0)

すべての実記事Learningは `learning/LEARNING_REGISTRY.json` で追跡し、Pattern Libraryへの昇格前に既存ルール照合を行います。
採用・却下・重複・実装・検証の履歴は `learning/DECISION_LOG.md` に残します。

## v2.4 Real-article Validation Patterns

| ID | Pattern | Canonical source |
|---|---|---|
| QP-013 | Before Source Integrity | `validation/real-article-publication-validation.md` |
| QP-014 | Paste-ready After and JSON Synchronization | `validation/real-article-publication-validation.md` |
| QP-015 | Search Demand Is Not Factual Evidence | `evidence/search-demand-evidence-boundary.md` |
| QP-016 | Low Sample Title Control | `patterns/low-sample-title-control-pattern.md` |
| QP-017 | Winner Query Protection | `patterns/winner-query-protection-pattern.md` |
| QP-018 | Supernatural Health Causation Guard | `knowledge/supernatural-health-causation-safety.md` |
| QP-019 | Conditional Food Safety Claims | `knowledge/food-safety-conditional-claims.md` |
| QP-020 | Internal Link Destination Validation | `knowledge/internal-link-destination-validation.md` |
| QP-021 | Title Promise Alignment | `knowledge/title-promise-alignment.md` |

| QP-022 | Revenue First Validation | `product/revenue-first-validation-principle.md` |
| QP-023 | Intent Drift Cross-Link Routing | `patterns/intent-drift-cross-link-pattern.md` |
