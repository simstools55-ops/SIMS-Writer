# ADR-0009: Decision Layer Between Knowledge and Pattern

## Status

Accepted

## Context

Knowledgeは判断根拠を、Patternは実行方法を提供するが、何を変更するかを正式に決定する責務が不足していた。Pattern Selectionだけでは不要な変更や過剰適用を防げない。

## Decision

Knowledge AssemblyとPattern Selectionの間にDecision Frameworkを設ける。

```text
Knowledge Assembly → Decision Evaluation → Action Plan → Pattern Selection
```

Decisionは変更の必要性、対象、範囲、優先度、非実施、手動確認を記録する。

## Consequences

- 不要なPattern適用を減らせる。
- no_changeを正式な結果として扱える。
- 判断理由を追跡できる。
- ContractとRuntime Stageが増えるが、Engine巨大化を回避できる。
