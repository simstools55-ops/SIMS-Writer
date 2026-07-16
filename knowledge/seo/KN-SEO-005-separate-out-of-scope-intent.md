---
id: KN-SEO-005
title: Separate Out-of-Scope Intent
category: seo
knowledge_type: decision_heuristic
version: 1.0.0
status: active
authority_level: A
confidence: verified
source_ids:
- SRC-QLT-001
applicability:
  request_types:
  - all
exceptions: []
related_quality_rules:
- QF-INT-003
- QF-SEO-004
related_patterns: []
reviewed_at: '2026-07-17'
next_review_at: '2027-01-17'
---

# Separate Out-of-Scope Intent

## Statement

主題から外れる検索意図は、別記事候補として分離する。

## Rationale

すべてのクエリを一記事へ混在させると主題と構造がぼやけるため。

## Application Notes

- 適用時はRequest Contextと例外条件を確認する。
- Quality Ruleの判定根拠として利用する場合は、Knowledge IDとVersionを記録する。
