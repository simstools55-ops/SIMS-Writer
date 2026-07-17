# SIMS Writer

SIMS Writerは、SIMS-Blog-Managerから受け取る改善依頼を、契約・知識・判断・パターン・品質ルールに基づいて処理し、公開判断付きの成果物へ変換する記事改善Runtimeです。

## Version

`1.10.0`

## Repository v1.10.0 の実装範囲

- SIMS-Blog-Manager / Generic JSONの自動判定・UTF-8 JSON読込
- Improvement Request Contract v1.0によるスキーマ検証
- 数値、CTRパーセント表記、重複クエリの安全な正規化
- 不変Article Contextの生成とRuntime成果物への接続
- HTML / Markdown / Plain Textの記事本文抽出
- はてなブログ・WordPress向けの広告、関連記事、共有UI、ナビゲーション等のノイズ除去
- 抽出プロファイルと除去件数をSource Snapshotへ記録
- URLからの公開記事本文取得（明示的な`--fetch-source`指定時のみ）
- HTTP/HTTPS制限、プライベートネットワーク拒否、2MB上限、Content-Type検証
- URL取得失敗時の安全な`manual_review_required`フォールバック
- 見出し、正規化本文、文字数、SHA-256を含むSource Snapshot生成
- 本文未提供時の明示的な`manual_review_required`判定
- メインクエリ・補助クエリに基づく決定的な検索意図分析
- 意図別クエリクラスタ、FAQ候補、見出し候補をContent Planへ接続
- 決定的CTR改善AdapterによるSEOタイトル・導入文・FAQ提案生成
- Before / Afterと変更理由を含む改善成果物
- 実行結果、Publication Package、完成記事Markdown、改善レポート、Execution Manifestの一括出力
- 成果物7点の自動検証、SHA-256チェックサム、公開可否判定
- 前回実行成果物の自動アーカイブと実行履歴管理
- 実行間のファイル・Publication Package差分比較
- 自動検証結果JSONと公開チェックリストMarkdownの生成
- 公開候補の保留・承認・却下・確定ワークフロー
- 承認履歴とExecution ID固定による誤公開防止
- 確定時の不変公開スナップショット生成
- Knowledge選択とContent PlanをRuntimeへ実接続
- 11 Stage Runtime Pipeline
- Contract / Knowledge / Decision / Pattern / Quality検証
- Targeted Refinement Runtime
- Provider-neutral Model Adapter基盤
- CTR Improvement Vertical Slice
- 12 Case Golden UAT
- SIMS-Core移行評価基盤
- Claude出力の既知の軽微な揺れ（camelCase、空白、限定ステータス表記）を安全に正規化
- 未知フィールドや根拠のない内容は正規化で隠さず拒否
- Claude Project Golden UAT 6ケースとCLI実行レポート
- 複数改善依頼JSONのフォルダ単位バッチ処理
- 記事ごとの独立出力、エラー分離、処理継続
- バッチ全体のJSON・Markdownサマリー生成

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

記事本文がJSONにない場合は、対象URLから取得できます。

```bash
python -m runtime.sims_writer_runtime.cli \
  --input examples/intake/sbm-improvement-request.json \
  --output runtime-output \
  --fetch-source
```

URL取得は明示指定時だけ有効です。取得できない場合は推測で進めず、手動確認が必要な状態として記録します。

記事本文を入力する場合は、JSONに次の項目を含めます。

```json
{
  "existing_content": "<article>...</article>",
  "content_format": "html"
}
```

`content_format`は`auto`、`html`、`markdown`、`plain_text`を利用できます。

実行後の出力フォルダには次の11ファイルが作成されます。

- `runtime-result.json`
- `publication-package.json`
- `article.md`
- `improvement-report.md`
- `execution-manifest.json`
- `artifact-validation.json`
- `publication-checklist.md`
- `artifact-diff.json`
- `execution-history.json`
- `publication-approval.json`
- `approval-history.json`

同じ出力先へ再実行すると、前回の主要成果物は`.history/<execution_id>/`へ自動保存されます。

## 複数記事のバッチ実行

改善依頼JSONを1つのフォルダに置き、まとめて実行できます。

```bash
python -m runtime.sims_writer_runtime.cli \
  --batch-input examples/batch/requests \
  --output batch-output
```

記事別成果物は`batch-output/items/<request-id>/`へ保存され、全体結果は`batch-summary.json`と`batch-summary.md`へ出力されます。1件が失敗しても、残りの記事処理は継続します。

## 公開承認と確定

生成直後は`pending_review`です。検証済み成果物だけを承認できます。

```bash
python -m runtime.sims_writer_runtime.cli --output runtime-output --approve --reviewer "reviewer-name"
```

却下には理由が必須です。

```bash
python -m runtime.sims_writer_runtime.cli --output runtime-output --reject --reviewer "reviewer-name" --reason "FAQの根拠を再確認"
```

承認後に確定すると、`release/<execution_id>/`へ公開スナップショットが保存されます。

```bash
python -m runtime.sims_writer_runtime.cli --output runtime-output --finalize --reviewer "reviewer-name"
```

確定時には`finalization-manifest.json`とSHA-256チェックサムが生成されます。

## CTR Vertical Slice実行

```bash
python tools/run_ctr_vertical_slice.py \
  examples/vertical-slices/ctr-improvement/sbm-request.json \
  --repo-root . \
  --output ctr-result.json
```


## Claude Project Golden UAT

Claude Project出力の受け入れ、安全拒否、既知の出力揺れへの耐性を固定ケースで検証できます。

```bash
python -m runtime.sims_writer_runtime.cli \
  --output claude-uat-output \
  --run-claude-uat
```

結果は`claude-uat-output/claude-golden-uat-report.json`へ保存されます。

## 開発方針

Repository全体をSingle Source of Truthとして管理します。SIMS-Coreの資産は構造をそのまま移植せず、Knowledge・Decision・Pattern・Quality Rule・Golden Caseとして評価して取り込みます。

### 公開版エクスポート

承認・確定済みの公開スナップショットから、外部配布用ZIPを生成できます。

```bash
python -m runtime.sims_writer_runtime.cli --output runtime-output --export
```

生成先は `runtime-output/distribution/` です。ZIPには公開成果物と `distribution-manifest.json` が含まれ、SHA-256で整合性を確認できます。


## Internal-link analysis

Supply `article_catalog` (or SBM `ArticleCatalog`) to select up to eight grounded internal-link candidates. Low-relevance supporting queries are kept separately as future article candidates.

### v1.10.0 Claude Developer Rehearsal

- Claude配布ファイルだけで行う操作リハーサル手順
- 記録用テストチェックリスト
- 配布ファイルのSHA-256 Manifest
- Claude専用配布ZIPの再現可能なビルドツール
- 利用者テスト開始条件の機械判定レポート

この版はDeveloper Rehearsalです。一般利用者テスト開始版ではありません。
