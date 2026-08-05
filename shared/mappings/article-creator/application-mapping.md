# SIMS Article Creator Application Mapping

SIMS Article Creatorは共通知識を新規記事設計へ適用する。

| 共通知識 | Article Creatorでの適用 |
|---|---|
| Intent Gap | 検索者の期待と実態の差を記事構造と導入で解決する |
| Hidden Anxiety | 判断に影響する未解決の不安を必要な見出し・FAQへ反映する |
| Evidence Transparency | 情報源の強さに応じて断定度と注記を調整する |
| SERP Entity Preservation | 主クエリを識別する固有語をタイトル・導入に保持する |
| Internal Link Semantics | 読者の次の疑問を補完するリンクだけを採用する |
| Decision Support | 比較表・条件別判断・向き不向きを必要に応じて設計する |

事実、体験、レビュー、価格、仕様、効果を創作しない。


## Shared v1.3.0 Common Validation Mapping

- VAL-FACT-001 数値整合性
- VAL-EVIDENCE-002 Evidence境界
- VAL-CAUSAL-001 因果表現
- VAL-CONSISTENCY-001 論理整合性
- VAL-ENTITY-001 HTML Entity整合性
- VAL-LINK-001 内部リンク整合性


## v2.1.0 Quality Pattern Library boundary

Article Creatorは製品中立Patternのみを利用する。既存記事のBefore/After、Preservation、Search Console固有判断はWriter専用であり適用しない。

## v3.0 compatibility mapping

Creator may consume confidence, source, contradiction, preservation, and learning-promotion rules. Temporal lifecycle recovery is used only when a new article covers a time-sensitive subject; it does not change Creator's new-article-only identity.
