---
id: KN-SEO-007
title: Main Query Field Is Pure
category: seo
knowledge_type: rule
version: 1.0.0
status: active
authority_level: B
confidence: verified
source_ids:
- SRC-KNW-001
applicability:
  request_types:
  - existing_article_improvement
exceptions: []
related_quality_rules: []
related_patterns: []
reviewed_at: '2026-07-17'
next_review_at: '2027-01-17'
---

# KN-SEO-007 Main Query Field Is Pure

## Rule

`new_values.main_query` には検索クエリ文字列だけを格納する。

メインクエリを本文やタイトルから推定した場合も、注記を同じフィールドへ混在させず、`main_query_source="estimated"` と `estimated_fields=["main_query"]` で明示し、補足説明は `information` に記録する。
