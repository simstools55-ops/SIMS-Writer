# Search Intent Analysis v1.0

SIMS Writerは、改善依頼に含まれるメインクエリと補助クエリだけを根拠として、検索意図を決定的に分類します。

## 出力

- primary: 主検索意図とラベル
- supporting: 補助クエリごとの意図
- intent_clusters: 意図別クエリ群
- faq_candidates: FAQ候補
- heading_recommendations: 見出し候補

外部検索結果を観察していないため、`analysis_basis` は常に `supplied_queries_only` として記録します。SERPを確認したという表現や、競合情報の推測は行いません。
