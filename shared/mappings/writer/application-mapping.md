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
