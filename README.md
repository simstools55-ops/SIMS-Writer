# SIMS Writer

SIMS Writerは、SIMS-Blog-Managerから受け取る改善依頼を、契約・知識・判断・パターン・品質ルールに基づいて処理し、公開判断付きの成果物へ変換する記事改善Runtimeです。

## Version

`0.1.0`

## Repository v0.1.0 の実装範囲

- 11 Stage Runtime Pipeline
- Generic JSON / SIMS-Blog-Manager Input Adapter
- 15 Contract Schema とExample Validation
- 28 Knowledge Assets / 12 Decision Definitions / 61 Pattern Definitions
- 42 Quality Rules / 13 Dimensions / 7 Quality Gates
- Targeted Refinement Runtime
- Provider-neutral Model Adapter基盤
- CTR Improvement Vertical Slice
- 12 Case Golden UAT
- SIMS-Core移行評価基盤

## セットアップ

```bash
python -m pip install -r requirements.txt
```

## Repository一括テスト

```bash
python -m pytest
```

## CTR Vertical Slice実行

```bash
python tools/run_ctr_vertical_slice.py \
  examples/vertical-slices/ctr-improvement/sbm-request.json \
  --repo-root . \
  --output ctr-result.json
```

## Runtime Core実行

```bash
python -m runtime.sims_writer_runtime.cli \
  --input examples/runtime/generic-request.json \
  --output runtime-output
```

## 開発方針

Repository全体をSingle Source of Truthとして管理します。SIMS-Coreの資産は構造をそのまま移植せず、Knowledge・Decision・Pattern・Quality Rule・Golden Caseとして評価して取り込みます。
