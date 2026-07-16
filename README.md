# SIMS Writer

SIMS Writerは、Quality Framework・Contracts・Knowledge・Decision Framework・Pattern Libraryを中核とし、Runtime CoreによってPublish Ready成果物へ接続する記事生成基盤です。

## Version

`0.7.0-alpha.1`

## このパッケージ

v0.6.0までの全資産に加え、実行可能なRuntime Coreの最小実装を収録します。

- 11 Stage Pipeline（Decision Evaluationを含む）
- Runtime Orchestrator / State Model
- Runtime Manifest / Asset Version Lock
- Execution Record / Error Mapping
- Generic JSON・SBM Input Adapter
- Manual Model Adapter（安全な構造検証用）
- Contract / Registry / Pipeline Validator
- Dry-run CLIとEnd-to-End Test

## 実行例

```bash
python -m runtime.sims_writer_runtime.cli \
  --input examples/runtime/generic-request.json \
  --output runtime-output
```

このAlphaでは、Runtime接続・状態遷移・追跡性を検証します。公開記事本文の本生成は次期Model Adapter Packageで実装します。

## 検証

```bash
python tools/validators/validate_runtime.py
python tests/runtime/test_runtime_core.py
python tests/contracts/test_contract_examples.py
```

SIMS Writer RepositoryをSingle Source of Truthとして管理します。
