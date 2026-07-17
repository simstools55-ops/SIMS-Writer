# SIMS Writer

SIMS Writerは、Quality Framework・Contracts・Knowledge・Decision Framework・Pattern Libraryを中核とし、Runtime CoreによってPublish Ready成果物へ接続する記事生成基盤です。

## Version

`0.14.3-alpha.1`

## このパッケージ

v0.13.0までの全資産に加え、実記事テスト8件を反映したProduction-grade Output Architectureを収録します。

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


## v0.9.0-alpha.1 Model Adapters

Claude Messages、OpenAI Responses、Generic Chat向けのProvider非依存Adapter基盤、Context Builder、JSON Output Parser、Fixture E2E Testを追加しました。外部APIキーとライブ接続は同梱していません。


## v0.9.0-alpha.1 Quality Validation Runtime

42件の正式Quality Rule、13 Dimension、7 GateをRuntimeで実行します。機械判定できない規則は `unable_to_verify` として可視化し、根拠のないPublish Ready判定を防ぎます。

## v0.11.0-alpha.1 Targeted Refinement

Quality Issueを対象Componentと原因Stageへ振り分け、安全な自動修正後に42 Quality Ruleを再実行します。事実や検索意図は推測で補わず、Targeted RevisionまたはManual Reviewとして残します。


## Golden UAT

```bash
python tools/uat/run_golden_uat.py
```

12の固定Caseで、Quality Rule・Gate・Refinement・Publish Decisionの回帰を確認します。


## v0.12 SIMS-Core Migration

SIMS-CoreからはArchitectureをコピーせず、Knowledge・Decision・Pattern・Quality Rule・Golden Caseとして有効な知見を評価移行します。暫定台帳は `migrations/sims-core/`、Lessons Learnedは `knowledge/lessons-learned/sims-core/` にあります。

## v0.13 CTR Vertical Slice

SBM形式JSONを使い、CTR改善のタイトル・導入・FAQ判断からQuality Validation、Publication Packageまでを実行できます。

```bash
python tools/run_ctr_vertical_slice.py examples/vertical-slices/ctr-improvement/sbm-request.json --repo-root . --output ctr-result.json
```


## v0.14 Output Architecture RC2

- 利用者向け出力とSIMS_FEEDBACK JSONを分離
- `summary / partial / full / publish / json_only` を正式化
- JSONを最終要素に固定し、変更フラグを実出力から導出
- 未確認の内部リンク採用と根拠のない数値予測を禁止
- メインクエリ未入力時は推定値と警告を分離

```bash
python tools/run_ctr_vertical_slice.py examples/vertical-slices/ctr-improvement/sbm-request.json --repo-root . --mode partial --output ctr-result.json
```
