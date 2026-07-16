# SIMS Writer

SIMS Writerは、Quality Framework・Contracts・Knowledge・Decision Framework・Pattern Libraryを中核とするPublish Ready記事生成基盤です。

## Version

`0.5.0-alpha.1`

## このパッケージ

v0.4.0までのFoundation、Contracts、Quality、Knowledgeに加え、判断を明示的な製品資産として扱うDecision Frameworkを実装しています。

- Decision Framework v1.0
- 12 Initial Decision Definitions
- 3 Decision Contracts / JSON Schemas
- Decision Registry
- Decision Policy / Conflict Policy / Explainability Policy
- Decision Validator / Automated Tests
- ADR-0009 Decision Layer Between Knowledge and Pattern

## 中核構造

```text
Quality Framework
Contracts
Knowledge
Decision Framework
Pattern Library
Runtime
```

## 検証

```bash
python tools/validators/validate_decisions.py
python tests/decisions/test_decision_assets.py
python tests/contracts/test_contract_examples.py
```

SIMS Writer RepositoryをSingle Source of Truthとして管理します。
