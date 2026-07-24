# Common Editorial Validation v1.0

| Code | Gate | Failure condition |
|---|---|---|
| VAL-FACT-001 | Fact | 数値・単位・期間・合計が矛盾する |
| VAL-EVIDENCE-002 | Evidence | 根拠範囲外の事実を追加する |
| VAL-CAUSAL-001 | Causality | 根拠なく因果を断定する |
| VAL-CONSISTENCY-001 | Consistency | セクション間で主張が矛盾する |
| VAL-ENTITY-001 | HTML | 二重Entity、文字化け、HTML破損がある |
| VAL-LINK-001 | Link | URL、タイトル、アンカー、プレースホルダーに欠陥がある |

公開判断に影響する違反だけをwarningまたはfailureとして出す。修正済みの指摘や単なる保留事項はinformationとして扱う。
