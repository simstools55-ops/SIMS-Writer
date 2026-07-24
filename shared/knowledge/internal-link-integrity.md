# VAL-LINK-001 内部リンク整合性

## 目的

WriterとArticle Creatorに共通する編集品質を安定させる。

## 規則

内部リンクのタイトル、URL、アンカーテキスト、文字コードを確認する。example.com、TODO、URL未確定、空URL、タイトルとURLの取り違えを公開用出力へ残さない。

## 適用

- Writer: 既存本文・改善案・改善後全文・内部リンク評価を照合する。
- Article Creator: Evidence Plan・生成本文・HTML出力を照合する。

## 製品境界

この規則はQuery Coverage、QUERY_MIX、Winner Query Preservation、SIMS_FEEDBACK_V2を定義しない。
