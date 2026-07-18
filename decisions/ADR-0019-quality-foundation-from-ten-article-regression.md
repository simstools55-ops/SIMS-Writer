# ADR-0019: Adopt a Quality Foundation from ten-article regression

## Status
Accepted

## Context
10件の実記事テストでは平均82.1点に到達した一方、数値整合、検索診断、Feedback Contractの不一致が繰り返された。

## Decision
既存の42 Quality Rulesを置き換えず、検索診断・Consistency Audit・Contract Validationを担うQuality Foundationを追加する。

## Consequences
- Runtimeはcanonical quality reportに加えてquality foundation reportを生成する。
- 外部Evidenceと内部リンクカニバリは次リリースで扱う。
- 既存出力形式との互換性を維持する。
