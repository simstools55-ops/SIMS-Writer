---
id: KN-OPS-004
title: Separate User Output and Feedback
category: operations
knowledge_type: principle
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

# KN-OPS-004 Separate User Output and Feedback

## Rule

利用者が読む改善案と、システムが読むFeedback JSONを別レイヤーとして扱う。

## Required behavior

- 利用者向けは Before / After / 理由を中心にする。
- Feedback JSONは変更フラグ、変更値、要約、警告に限定する。
- 全文は明示要求時だけ出力する。
- JSONは必ず最後に置き、その後に文章を出さない。

## Evidence

2026-07-17の実記事テスト8件で、全文とJSONの重複、JSON順序違反、利用者が修正箇所を見つけにくい問題が再発した。A000007の部分出力形式が最も高い利用者評価を得た。
