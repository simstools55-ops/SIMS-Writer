---
id: KN-OPS-001
title: Targeted Revision Before Full Rewrite
category: operations
knowledge_type: operational_principle
version: 1.0.0
status: active
authority_level: A
confidence: verified
source_ids:
- SRC-PRD-002
- SRC-OPS-001
applicability:
  request_types:
  - existing_article_improvement
exceptions: []
related_quality_rules:
- QF-SIT-002
related_patterns: []
reviewed_at: '2026-07-17'
next_review_at: '2027-01-17'
---

# Targeted Revision Before Full Rewrite

## Statement

既存記事の問題が部分的なら、対象箇所の修正を全文再生成より優先する。

## Rationale

追加編集量と回帰リスクを抑えやすいため。

## Application Notes

- 適用時はRequest Contextと例外条件を確認する。
- Quality Ruleの判定根拠として利用する場合は、Knowledge IDとVersionを記録する。
