# VAL-FACT-001 数値整合性

## 目的

WriterとArticle Creatorに共通する編集品質を安定させる。

## 規則

数値、単位、期間、合計、割合、換算結果を相互照合する。入力または根拠から再計算できない数値は断定しない。矛盾が公開判断へ影響する場合はFAIL、軽微で修正可能ならPASS_WITH_WARNINGとする。

## 適用

- Writer: 既存本文・改善案・改善後全文・内部リンク評価を照合する。
- Article Creator: Evidence Plan・生成本文・HTML出力を照合する。

## 製品境界

この規則はQuery Coverage、QUERY_MIX、Winner Query Preservation、SIMS_FEEDBACK_V2を定義しない。
