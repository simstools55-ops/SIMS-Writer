# ADR-0017: CTR Improvement as First Vertical Slice

- Status: Accepted
- Date: 2026-07-17

## Decision

Product 1.0の最初の実用Vertical SliceをCTR改善に限定し、SBM JSONからPublication Packageまでを一度通す。

## Rationale

CTR改善はGSC指標で対象選定と効果測定がしやすく、SIMS-Coreとの比較にも適している。全Knowledge・Decision・Patternを一度に実装せず、タイトル、導入、FAQの判断に限定する。

## Consequences

- 外部LLMなしでEnd-to-Endの接続を検証できる。
- 決定論的生成は最終品質の完成形ではない。
- Betaでは実記事とModel Adapterを使用して比較評価する。
