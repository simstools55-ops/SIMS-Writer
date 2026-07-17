# Output Contract v1.1

## Purpose

利用者向け成果物と `SIMS_FEEDBACK_V1` を分離し、実記事テストで確認された重複・順序違反・変更フラグ不整合を防止する。

## Output Order

1. 利用者向け改善案
2. 内部リンク評価
3. 確認事項
4. `SIMS_FEEDBACK_V1` JSON
5. 終了

JSONの後には文章を出力しない。

## Output Modes

- `summary`: 改善概要のみ
- `partial`: 変更箇所を Before / After / 理由で出力する既定モード
- `full`: 変更箇所に加え記事全文を出力
- `publish`: 公開用記事全文とメタ情報を出力
- `json_only`: Feedback JSONのみ

`article_content` は `full` または `publish` の場合だけ許可する。

## Human-facing Format

各変更は次の順序を固定する。

- 対象
- Before
- After
- 理由

本文へ新しい説明ブロックを追加した場合は `changes.body=true` とする。FAQだけの追加は `changes.faq=true` であり、通常本文を追加しない限り `body=false` を維持する。

## Feedback Rules

- `main_query` は検索クエリ文字列だけを格納する。
- 推定・要確認などの注記は `warnings` に格納する。
- 根拠のないCTR・クリック数の数値予測は禁止する。
- JSONは機械連携用の要約であり、記事全文や長い評価レポートを格納しない。
