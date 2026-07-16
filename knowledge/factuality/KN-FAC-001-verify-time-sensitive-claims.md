---
id: KN-FAC-001
title: Verify Time-Sensitive Claims
category: factuality
knowledge_type: rule_basis
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
- QF-FAC-001
related_patterns: []
reviewed_at: '2026-07-17'
next_review_at: '2027-01-17'
---

# Verify Time-Sensitive Claims

## Statement

料金・仕様・制度・最新機能など変化しうる重要情報は、確認日付きの信頼できるSourceで検証する。

## Rationale

古い情報を最新情報として断定することを防ぐため。

## Application Notes

- 適用時はRequest Contextと例外条件を確認する。
- Quality Ruleの判定根拠として利用する場合は、Knowledge IDとVersionを記録する。
