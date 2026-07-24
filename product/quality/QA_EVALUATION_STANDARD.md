# SIMS Writer QA Evaluation Standard v1.0

## Purpose
Claudeが作成したBefore/After改善案を公開直前に評価し、公開可否を一貫して判定する。

## Evaluation order
1. Safety and YMYL
2. Article factual and numeric integrity
3. Search intent and SEO judgement
4. Winner Query preservation
5. Editorial preservation
6. Internal-link integrity
7. Contract conformance
8. Validation self-consistency
9. Regression protection

## Verdict rules
- `PASS`: 修正不要で公開可能。
- `PASS_WITH_WARNING`: 公開可能。測定不足、確認不能などの注意を残す。
- `PASS_WITH_MINOR_FIX`: QAが許可済み局所修正を適用し、再評価後に公開可能。
- `PASS_WITH_REQUIRED_FIX`: 公開停止。主要な不整合を直して再評価する。
- `FAIL`: 公開停止。改善案の再生成または人の判断が必要。

## Required checks
### Article quality
- タイトル、メタ、導入、見出し、FAQ、本文の相互整合。
- 数値、単位、期間、割合、月額・年額の再計算。
- 根拠を超える断定、未確認の原因説明、本文にない情報の追加を禁止。

### SEO judgement
- Query Coverageが低いときは断定しない。
- Winner Queryを不必要に削除しない。
- QUERY_MIX_EFFECTを一つの記事へ無理に統合しない。
- LOW_SAMPLEでは変更量を抑える。

### Editorial preservation
- 体験談、独自レビュー、広告、比較表、画像、結論を保護する。
- QAは第二のWriterにならず、局所欠陥だけを直す。

### Internal links
- 意味的関連性、リンク先確認状態、実装状態を分離する。
- 未確認候補を`implemented`にしない。
- 全件不採用も正当な結果として記録する。

### Contract
- `format: SIMS_FEEDBACK_V2`、`contract_version: 2.1`を必須とする。
- `main_query`、構造化`query_coverage`、`changes[]`、`internal_link_evaluation`、`validation`を確認する。
- 空文字、旧`version`、Boolean changes、命名揺れを禁止する。

### Validation
- 検出済み不整合がある状態でPASSを出さない。
- WarningとPASS条件、本文とJSON、実装状態を相互照合する。

## Auto-fix boundary
自動修正可能: 誤字、助詞、明確な計算誤り、断定緩和、空文字除去、Contract正規化、状態値修正。
自動修正禁止: 検索意図変更、主要結論変更、体験談改変、新事実追加、YMYL判断、Winner Query破壊。
