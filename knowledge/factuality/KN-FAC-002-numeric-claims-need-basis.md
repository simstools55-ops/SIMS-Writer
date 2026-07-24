---
id: KN-FAC-002
title: Numeric Claims Need Basis
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
- QF-FAC-002
related_patterns: []
reviewed_at: '2026-07-17'
next_review_at: '2027-01-17'
---

# Numeric Claims Need Basis

## Statement

数値・割合・期間・料金は、出典、計算過程、条件のいずれかを示せる状態にする。

## Rationale

根拠不明の数字は説得力ではなく誤情報リスクを増やすため。

## Application Notes

- 適用時はRequest Contextと例外条件を確認する。
- Quality Ruleの判定根拠として利用する場合は、Knowledge IDとVersionを記録する。
