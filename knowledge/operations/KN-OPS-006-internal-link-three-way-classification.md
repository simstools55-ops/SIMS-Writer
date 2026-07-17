---
id: KN-OPS-006
title: Internal Link Three-way Classification
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

# KN-OPS-006 Internal Link Three-way Classification

## Rule

内部リンク候補は `採用 / 保留 / 不採用` の3分類で評価する。

- 採用: 検索意図と本文の流れが一致し、URLと記事タイトルを確認済みで、実際に挿入する。
- 保留: 関連性はあるがURL・タイトル・設置根拠のいずれかが未確認。
- 不採用: 検索意図または本文の流れに合わない。

URLまたはタイトルを確認できない候補はHTMLリンクとして出力しない。
