# ADR-0011 Runtime Core as Contract-Controlled Pipeline

## Status
Accepted

## Decision
RuntimeをEngine群ではなく、Decision Evaluationを含む11 StageのContract制御Pipelineとして実装する。生成モデルはAdapterへ隔離する。

## Consequences
- Stage単位の検証・再開・差し替えが可能になる。
- Product Coreの正式資産をRuntime都合で変更しない。
- Alpha 1では公開記事生成を実装済みと見せず、接続と追跡性の検証に限定する。
