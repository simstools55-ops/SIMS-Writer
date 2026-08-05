---
id: KN-SEO-001
title: Primary Intent Before Structure
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
  - new_article
  - existing_article_improvement
exceptions: []
related_quality_rules:
- QF-INT-001
- QF-INT-002
related_patterns: []
reviewed_at: '2026-07-17'
next_review_at: '2027-01-17'
---

# Primary Intent Before Structure

## Statement

見出し構成を作る前に、メインクエリのPrimary Intentを明確にする。

## Rationale

検索意図が未確定の構成は情報量があっても主目的を外しやすいため。

## Application Notes

- 適用時はRequest Contextと例外条件を確認する。
- Quality Ruleの判定根拠として利用する場合は、Knowledge IDとVersionを記録する。
