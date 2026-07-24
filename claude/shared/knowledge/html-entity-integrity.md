# KN-ENTITY-001 / VAL-ENTITY-001 HTML Entity整合性

## 目的

WriterとArticle Creatorが生成するタイトル、メタディスクリプション、本文、FAQ、内部リンクで、HTML Entityの二重エンコードと文字化けを防止する。

## 規則

- `&quot;`、`&amp;`、`&lt;`、`&gt;`などを、表示用テキストの中で不用意に再エンコードしない。
- `&amp;quot;`、`&amp;amp;`、`&amp;lt;`、`&amp;gt;`は二重エンコード候補として検出する。
- メタディスクリプションでは、引用符が必要な場合は原則として日本語の括弧記号（「」または『』）を使用できる。
- 既存入力にEntityが含まれる場合、保存先のHTML処理を考慮せず機械的に再エンコードしない。
- 未閉鎖Entity、置換文字`�`、典型的な文字化け、不要なMarkdown混入も検出対象とする。

## Validation

違反または未解決の疑いがある場合は`VAL-ENTITY-001`をFAILまたはWARNINGとして記録する。修正後の値に二重エンコードが残っていない場合だけPASSとする。

## 適用

- Writer: 既存本文、改善案、改善後全文、SEOタイトル、メタディスクリプション、内部リンク評価を照合する。
- Article Creator: Evidence Plan、生成本文、HTML出力、内部リンク出力を照合する。

## 製品境界

この規則はQuery Coverage、QUERY_MIX、Winner Query Preservation、SIMS_FEEDBACK_V2を定義しない。
