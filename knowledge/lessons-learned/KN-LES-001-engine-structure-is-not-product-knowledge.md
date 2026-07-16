---
id: KN-LES-001
title: Engine Structure Is Not Product Knowledge
category: lessons-learned
knowledge_type: lesson_learned
version: 1.0.0
status: review
authority_level: A
confidence: verified
source_ids:
- SRC-PRD-002
- SRC-OPS-001
applicability:
  request_types:
  - migration
exceptions: []
related_quality_rules: []
related_patterns: []
reviewed_at: '2026-07-17'
next_review_at: '2027-01-17'
---

# Engine Structure Is Not Product Knowledge

## Statement

SIMS-CoreのEngine番号やPrompt配置は参考資料であり、SIMS Writerの正式Knowledgeとして継承しない。

## Rationale

旧実装構造を知識と混同すると、新アーキテクチャを歪めるため。

## Application Notes

- 適用時はRequest Contextと例外条件を確認する。
- Quality Ruleの判定根拠として利用する場合は、Knowledge IDとVersionを記録する。
