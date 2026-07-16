# ADR-0016: Migrate SIMS-Core Knowledge, Not Its Architecture

- Status: Accepted
- Date: 2026-07-17

## Context

SIMS-Coreには検索意図、既存価値保存、日本語品質、管理用構造化出力などの有効な知見がある。一方、Engine中心構造、固定Workflow、Prompt内の重複ルールはSIMS Writerの設計原則と一致しない。

## Decision

SIMS-Coreからは知識、判断、成功・失敗例、出力要件を抽出して移行する。Engine構造、固定出力順、モデル固有PromptをArchitectureとして継承しない。

## Consequences

- 移行には抽出と再検証が必要で、単純コピーより時間がかかる。
- 新製品の責務境界とモデル独立性を維持できる。
- 旧資産と新資産の対応をMigration Inventoryで追跡する。
