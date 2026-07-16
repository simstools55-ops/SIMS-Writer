---
id: KN-FAC-004
title: Unable to Verify Must Remain Visible
category: factuality
knowledge_type: warning
version: 1.0.0
status: active
authority_level: A
confidence: verified
source_ids:
- SRC-PRD-002
- SRC-QLT-001
applicability:
  request_types:
  - all
exceptions: []
related_quality_rules:
- QF-PUB-003
- QF-FAC-001
related_patterns: []
reviewed_at: '2026-07-17'
next_review_at: '2027-01-17'
---

# Unable to Verify Must Remain Visible

## Statement

重要情報を確認できない場合は、削除・限定表現・要確認のいずれかで扱い、推測で埋めない。

## Rationale

検証不能を隠すとPublish Ready判定が不正確になるため。

## Application Notes

- 適用時はRequest Contextと例外条件を確認する。
- Quality Ruleの判定根拠として利用する場合は、Knowledge IDとVersionを記録する。
