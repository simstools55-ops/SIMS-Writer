# SIMS Writer v3.5.1

## Fix
- 内部リンクを採用したAfterには、リンク先URLを含む実リンクを必須化しました。
- アンカーテキストだけ、記事名だけ、URLなしのAfterをPUBLIC_OKにすることを禁止しました。
- HTML/Markdownは元記事形式を維持し、利用者にhref追加の手作業を残しません。
- 表示用Before/AfterとSBM返却JSONのAfterを同じリンク実装済み内容へ同期します。

Personal Knowledge候補生成、Writer契約、Shared v3.5.1互換性は変更ありません。
