# VAL-ENTITY-001 HTML Entity整合性

## 目的

WriterとArticle Creatorに共通する編集品質を安定させる。

## 規則

&amp;amp;、&amp;lt;等の二重エンコード、文字化け、未閉鎖Entity、不要なMarkdown混入を検出する。

## 適用

- Writer: 既存本文・改善案・改善後全文・内部リンク評価を照合する。
- Article Creator: Evidence Plan・生成本文・HTML出力を照合する。

## 製品境界

この規則はQuery Coverage、QUERY_MIX、Winner Query Preservation、SIMS_FEEDBACK_V2を定義しない。
