# ADR-0010 Decision-Gated Pattern Selection

## Status
Accepted

## Decision
Pattern SelectionはDecision Action Planの後にのみ実行する。no_changeまたはpreserve判定のComponentへ生成・改善Patternを適用しない。

## Rationale
Patternの過剰適用、不要な全面改稿、Engine中心設計の再発を防ぐため。
