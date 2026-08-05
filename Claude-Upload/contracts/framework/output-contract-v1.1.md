# Output Contract v1.4

## Purpose

利用者向け成果物と `SIMS_FEEDBACK_V2` を分離し、実記事テストで確認された重複・順序違反・変更フラグ不整合を防止する。

## Output Order

1. 利用者向け改善案
2. 内部リンク評価
3. 確認事項
4. `SIMS_FEEDBACK_V2` JSON
5. 終了

JSONの後には文章を出力しない。

## Output Modes

- `summary`: 改善概要のみ
- `partial`: 変更箇所を Before / After / 理由で出力する既定かつ正式な主力モード。既存のアフィリエイトリンク、ブログカード、広告、装飾、独自HTMLを保護する
- `full`: 変更箇所に加え記事全文を出力するベータモード
- `publish`: 公開候補の記事全文とメタ情報を出力するベータモード。入力で確認できない埋め込み要素の完全保持を保証しない
- `json_only`: Feedback JSONのみ

`article_content` は `full` または `publish` の場合だけ許可する。

## Human-facing Format

各変更は次の順序を固定する。

- 対象
- Before
- After
- 期待する効果
- 理由

本文へ新しい説明ブロックを追加した場合は `changes.body=true` とする。FAQだけの追加は `changes.faq=true` であり、通常本文を追加しない限り `body=false` を維持する。

## Feedback Rules

- `main_query` は検索クエリ文字列だけを格納する。
- 改善結果の安全性・正確性・反映判断に注意が必要な事項だけを `warnings` に格納する。
- 推定した事実、任意入力の不足による通常スキップ、現状維持の補足は `information` に格納する。
- `main_query_source` は `search_console` / `manual` / `estimated` / `unavailable` のいずれかとする。
- `execution_mode` は `standard` または `graceful_degradation` とする。
- 推定値は `estimated_fields` にフィールド名を列挙する。
- 根拠のないCTR・クリック数の数値予測は禁止する。
- JSONは機械連携用の要約であり、記事全文や長い評価レポートを格納しない。


## Presentation Guard

- 成果物は最初の見出しまたは本文から開始する。
- 挨拶、了承文、利用者への呼称を成果物の前に置かない。
- SEOタイトルは40文字以内を推奨、45文字を上限とする。
- メタディスクリプションは120文字以内を推奨、140文字を上限とする。
- `SIMS_FEEDBACK_V2` は回答内で1つだけの `json` 言語指定付きコードブロックにする。
- JSONコードブロックは回答の最終要素とし、閉じフェンス後に文字を置かない。

## Mode Positioning

Product 1.0では `partial` を正式な主力機能とする。`full` と `publish` は、変更量が多い場合の作業負担を減らすベータ機能とする。記事構造保持型の全文生成は将来機能とし、アフィリエイトリンク、ブログカード、広告、装飾、独自HTMLを保持できることを検証してから正式化する。


## User-Provided JSON Contract Priority (v0.14.3)

When the request includes an explicit JSON template or schema, that contract overrides the SIMS default feedback shape. The response must preserve exact field names, nesting, value types, required fields, enum constraints, and field order. Contract-external fields are prohibited. The JSON must be the single final fenced `json` block with no trailing content.

## RC3 Publish Quality

- 出力前に改善必要度を改善推奨・軽微改善・現状維持推奨の3段階で判定する。
- 検索意図を分類し、比較記事では比較項目・おすすめの人・最終結論の整合性を確認する。
- 変更箇所ごとに定性的な期待効果を示す。
- 変更しない主要箇所は、必要に応じて変更しない理由を示す。
- 反映作業の目安時間を提示する。
