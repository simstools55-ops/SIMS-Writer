---
id: KN-OPS-005
title: Change Flags Must Match Output
category: operations
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

# KN-OPS-005 Change Flags Must Match Output

## Rule

`SIMS_FEEDBACK_V1.changes` は実際に出力・適用した変更と一致させる。

## Examples

- 新しい本文ブロックを追加: `body=true`
- FAQだけを追加: `faq=true`, `body=false`
- 内部リンクを評価しただけ: `internal_links=false`
- 検証済みリンクを実際に挿入: `internal_links=true`

変更フラグを手書き判断だけに依存せず、Before/Afterと追加要素から導出する。
