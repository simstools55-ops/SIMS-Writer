---
id: KN-OPS-002
title: Track Before and After
category: operations
knowledge_type: process
version: 1.0.0
status: active
authority_level: A
confidence: verified
source_ids:
- SRC-DOM-001
- SRC-PRD-002
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

# Track Before and After

## Statement

既存記事改善では、保存・修正・追加・削除した要素と理由を追跡する。

## Rationale

改善の妥当性と回帰を後から検証できるようにするため。

## Application Notes

- 適用時はRequest Contextと例外条件を確認する。
- Quality Ruleの判定根拠として利用する場合は、Knowledge IDとVersionを記録する。
