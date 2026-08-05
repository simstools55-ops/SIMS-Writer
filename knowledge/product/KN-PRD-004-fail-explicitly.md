---
id: KN-PRD-004
title: Fail Explicitly
category: product
knowledge_type: rule_basis
version: 1.0.0
status: active
authority_level: A
confidence: verified
source_ids:
- SRC-PRD-002
applicability:
  request_types:
  - all
exceptions: []
related_quality_rules:
- QF-PUB-003
related_patterns: []
reviewed_at: '2026-07-17'
next_review_at: '2027-01-17'
---

# Fail Explicitly

## Statement

入力不足・検証不能・処理失敗を正常完了として扱わない。

## Rationale

問題を隠した成果物は公開判断を誤らせるため。

## Application Notes

- 適用時はRequest Contextと例外条件を確認する。
- Quality Ruleの判定根拠として利用する場合は、Knowledge IDとVersionを記録する。
