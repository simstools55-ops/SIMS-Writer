---
id: KN-FAC-005
title: No Unsupported Performance Forecast
category: factuality
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

# KN-FAC-005 No Unsupported Performance Forecast

## Rule

CTRやクリック数の具体的な改善幅は、比較可能な実測データまたは明示された根拠がない限り予測しない。

## Safe expression

- 「CTR改善余地がある」
- 「再測定で確認する」
- 「母数が小さいため定量予測は困難」

## Unsafe expression

- 根拠なしに「2〜3%へ改善」
- 根拠なしに「+1〜2クリック」
