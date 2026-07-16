# SIMS Writer

SIMS Writerは、Quality Framework・Contracts・Knowledge・Pattern Libraryを中核とするPublish Ready記事生成基盤です。

## Version

`0.4.0-alpha.1`

## このパッケージ

FoundationとContract Schemaに加え、Product 1.0の初期Quality Rules Packageを収録しています。

- 13 Quality Dimensions
- 42 Quality Rules
- 7 Quality Gates
- Rule/Gate Registry
- オフライン検証ツール

## 検証

```bash
python tools/validators/validate_quality_rules.py
python tests/contracts/test_contract_examples.py
```

SIMS Writer RepositoryをSingle Source of Truthとして管理します。


## v0.4.0-alpha.1 Initial Knowledge

- 28 initial Knowledge Items
- 10 Knowledge Sets
- Source / Knowledge / Set registries
- Knowledge validation tool
