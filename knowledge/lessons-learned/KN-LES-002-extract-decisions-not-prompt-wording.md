---
id: KN-LES-002
title: Extract Decisions, Not Prompt Wording
category: lessons-learned
knowledge_type: lesson_learned
version: 1.0.0
status: review
authority_level: C
confidence: medium
source_ids:
- SRC-KNW-001
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

# Extract Decisions, Not Prompt Wording

## Statement

SIMS-Coreからは有効な判断・失敗防止・品質原則を抽出し、Prompt文そのものはRuntime参考として扱う。

## Rationale

モデル固有の表現より、再利用可能な知見を継承するため。

## Application Notes

- 適用時はRequest Contextと例外条件を確認する。
- Quality Ruleの判定根拠として利用する場合は、Knowledge IDとVersionを記録する。
