# SIMS Writer Decision Framework v1.0

## 1. 目的

Decision Frameworkは、Knowledgeを根拠として「何を行うか・行わないか・どこまで行うか」を決定し、必要なPatternだけを選択可能にする判断層である。

Decisionは文章生成ではなく、改善対象・処理範囲・優先順位・停止条件を確定する。

```text
Writing Request
+ Source Snapshot
+ Knowledge Assembly
+ Performance Data
+ Quality State
↓
Decision Context
↓
Decision Evaluation
↓
Decision Record
↓
Action Plan
↓
Pattern Selection
```

## 2. 基本原則

1. **Evidence before Action** — 根拠なしに変更を決めない。
2. **No Change is a Valid Decision** — 変更不要も正式な判断とする。
3. **Minimum Necessary Change** — 最小限の有効な変更を優先する。
4. **Preserve Proven Value** — 既存の強みを先に特定する。
5. **Explain Every Material Decision** — 重要判断には理由と根拠を残す。
6. **Separate Decision from Pattern** — Decisionは何をするか、Patternはどう実行するかを担う。
7. **Uncertainty is Explicit** — 判断不能を推測で埋めない。
8. **Quality Gates Override Optimization** — Safety・Factuality・Primary IntentをSEO施策より優先する。

## 3. Decisionの種類

- scope_decision
- component_decision
- preservation_decision
- evidence_decision
- seo_decision
- structure_decision
- faq_decision
- internal_link_decision
- publication_decision
- escalation_decision

## 4. Decision結果

- apply
- preserve
- revise
- add
- remove
- verify
- defer
- separate_article
- no_change
- manual_review
- reject

## 5. 判断材料

Decisionは最低限、次を参照できる。

- Writing Request
- Source Content Snapshot
- Performance Data
- Search Intent Model
- Knowledge Assembly
- Site Knowledge
- Quality Report
- Existing Article Index

## 6. 判断の出力

各Decisionは次を明示する。

- decision_id
- decision_type
- subject
- result
- rationale
- evidence
- confidence
- risks
- constraints
- required_actions
- prohibited_actions
- selected_pattern_categories
- manual_review_required

## 7. DecisionとPatternの境界

### Decision

- タイトルを変更するか
- FAQを追加するか
- 全文改稿が必要か
- 別記事に分けるか
- 公式情報確認が必要か

### Pattern

- 低CTRタイトルをどう改善するか
- FAQをどう本文と重複させず追加するか
- 既存価値をどう保存して修正するか

## 8. Decision Gate

Pattern Selectionへ進むには次を満たす。

- 必須Decisionが完了
- Blocked Decisionなし
- 重大な判断競合なし
- Confidenceが許容範囲
- Manual Review条件が解決済み、または明示済み
- Action Planが生成済み

## 9. Product 1.0の必須Decision

- DEC-SCP-001 Article Scope Decision
- DEC-IMP-001 Change Scope Decision
- DEC-IMP-002 Full Rewrite Necessity Decision
- DEC-SEO-001 Title Change Decision
- DEC-SEO-002 H1 Change Decision
- DEC-STR-001 Introduction Change Decision
- DEC-STR-002 Heading Reorganization Decision
- DEC-FAQ-001 FAQ Necessity Decision
- DEC-EVD-001 Evidence Verification Decision
- DEC-LNK-001 Internal Link Action Decision
- DEC-SEP-001 Separate Article Decision
- DEC-PUB-001 Publication Escalation Decision

## 10. Statement

> SIMS Writerは、Knowledgeから直接Patternへ進まず、Decision Frameworkによって変更の必要性・範囲・優先順位を明示的に判断し、必要な処理だけを実行する。
