# Real Article Publication Validation v2.4

実記事運用で公開可能な修正を一度で完成させるための最終検証正本です。

## VAL-REAL-001 Before Source Integrity

`before` は必ず依頼入力または取得済み実記事に存在する、変更前の全文でなければならない。
次の場合はその項目を `public_ok_changes` へ出力しない。

- 省略記号、要約、`以下略`、`…` を含む
- 前回提案のAfterをBeforeとして再利用している
- Writerが推測・補完した
- 実記事由来か判定できない
- 新規追加なのに既存文を捏造した

新規追加の標準表現は、対象に応じて次を使う。

- `（該当項目なし・新規追加）`
- `（FAQセクションなし・新規追加）`
- `（内部リンクなし・新規追加）`

## VAL-REAL-002 Paste-ready After

`after` は利用者がそのまま貼り付けられる完成文全文とする。作業指示、要約、差分説明、挿入指示だけを格納してはならない。

## VAL-REAL-003 Cross-output Synchronization

最終表示文、`publication_result.public_ok_changes`、`new_values`、`change_summary` は同じ最終状態を表さなければならない。局所修正のたびに全箇所を再同期する。

## VAL-REAL-004 Existing-state Reset

修正依頼を受けた際は、前回回答ではなく実記事の初期状態へ戻ってBeforeを確定する。実記事全文が欠ける場合は、該当コンポーネントのみ保留し、他の確定済み項目を出力できる。

## Required audit order

1. 実記事の変更前状態を確定
2. 変動情報と公式根拠を確認
3. タイトル・メタ・導入・本文・FAQ・CTAの意味整合を確認
4. Before全文を照合
5. After完成文を確認
6. 公開表示とJSONを同期
7. new_valuesとchange_summaryを同期
8. 最終出力
