# SIMS Writer

SIMS Writerは、SIMS-Blog-Managerから受け取る改善依頼を、契約・知識・判断・パターン・品質ルールに基づいて処理し、公開判断付きの成果物へ変換する記事改善Runtimeです。

## Version

`0.6.0`

## Repository v0.6.0 の実装範囲

- SIMS-Blog-Manager / Generic JSONの自動判定・UTF-8 JSON読込
- Improvement Request Contract v1.0によるスキーマ検証
- 数値、CTRパーセント表記、重複クエリの安全な正規化
- 不変Article Contextの生成とRuntime成果物への接続
- HTML / Markdown / Plain Textの記事本文抽出
- 見出し、正規化本文、文字数、SHA-256を含むSource Snapshot生成
- 本文未提供時の明示的な`manual_review_required`判定
- 決定的CTR改善AdapterによるSEOタイトル・導入文・FAQ提案生成
- Before / Afterと変更理由を含む改善成果物
- 実行結果、Publication Package、完成記事Markdown、改善レポート、Execution Manifestの一括出力
- 成果物7点の自動検証、SHA-256チェックサム、公開可否判定
- 自動検証結果JSONと公開チェックリストMarkdownの生成
- Knowledge選択とContent PlanをRuntimeへ実接続
- 11 Stage Runtime Pipeline
- Contract / Knowledge / Decision / Pattern / Quality検証
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
python tools/test_repository.py
```

## 改善依頼JSONの実行

入力形式は自動判定されます。

```bash
python -m runtime.sims_writer_runtime.cli \
  --input examples/intake/sbm-improvement-request.json \
  --output runtime-output
```

記事本文を入力する場合は、JSONに次の項目を含めます。

```json
{
  "existing_content": "<article>...</article>",
  "content_format": "html"
}
```

`content_format`は`auto`、`html`、`markdown`、`plain_text`を利用できます。

実行後の出力フォルダには次の7ファイルが作成されます。

- `runtime-result.json`
- `publication-package.json`
- `article.md`
- `improvement-report.md`
- `execution-manifest.json`
- `artifact-validation.json`
- `publication-checklist.md`

## CTR Vertical Slice実行

```bash
python tools/run_ctr_vertical_slice.py \
  examples/vertical-slices/ctr-improvement/sbm-request.json \
  --repo-root . \
  --output ctr-result.json
```

## 開発方針

Repository全体をSingle Source of Truthとして管理します。SIMS-Coreの資産は構造をそのまま移植せず、Knowledge・Decision・Pattern・Quality Rule・Golden Caseとして評価して取り込みます。
