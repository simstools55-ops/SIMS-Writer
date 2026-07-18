# Runtime Health Specification v1.0

## 目的
判定プロセスの健全性を開発・保守向けに要約する。

## status
- HEALTHY
- HEALTHY_WITH_WARNINGS
- REVIEW_NEEDED
- UNHEALTHY

## 必須フェーズ
- Contract Validation
- Search Diagnosis
- Consistency Audit
- Evidence Audit
- Coverage Audit
- Improvement Strategy

## Confidenceとの違い
Confidenceは判定の確からしさ、Runtime Healthは処理全体の正常性。

## 推奨ログ
- version
- execution timestamp
- ArticleID
- decision
- counts
- confidence
- risk
- triggered rule codes

内部思考・不要な全文・秘密情報は保持しない。
