# Coverage Audit Runtime Specification v1.0

## 1. 役割

Coverage Auditは、記事が検索意図へ答えるために必要な情報を、過不足なく含んでいるかを評価する。

網羅性を増やすこと自体が目的ではない。検索意図に不要な情報を増やさない。

## 2. 入力

- main_query
- top_queries
- search_intent
- article_type（利用可能な場合）
- article_title
- headings
- body
- faq
- Search Diagnosis
- Consistency Audit

## 3. Expected Topic Set

検索意図から、期待される論点を内部生成する。

例：

```text
main_query: Wi-Fi 電気代
```

期待論点候補：

- 月額の目安
- 年間の目安
- 消費電力からの計算方法
- つけっぱなし時の考え方
- 機種差
- 節約方法
- 電気代が急に増えた場合の確認点

すべてを必須にはしない。

## 4. Topic分類

### Required

検索意図へ直接答えるために必須。

### Recommended

読者の理解・判断を助ける。

### Optional

記事の独自性や補足として有用。

### Out of Scope

検索意図から外れる。追加しない。

## 5. Coverage Score

次の配点で評価する。

- Required topics：70点
- Recommended topics：20点
- 質問への直接回答：10点

Optional topicsは加点しない。過剰追加を防ぐためである。

## 6. 減点

- Required topic欠落：1件につき-15〜-30
- 結論が遅い：-5〜-10
- 検索意図と異なる説明が中心：-20
- 重複説明が多い：-5〜-15
- Out of Scopeが本文の20%以上：-10
- FAQのみで必須回答している：-5

## 7. 内部出力

```json
{
  "coverage_audit": {
    "score": 82,
    "status": "pass_with_suggestions",
    "required_topics": [
      {
        "topic": "月額の目安",
        "status": "covered"
      },
      {
        "topic": "計算方法",
        "status": "partial"
      }
    ],
    "recommended_topics": [],
    "out_of_scope_topics": [],
    "missing_topics": ["計算式の具体例"]
  }
}
```

## 8. 判定

- 90〜100：十分
- 75〜89：局所改善
- 60〜74：本文改善
- 40〜59：構成再設計候補
- 0〜39：全面再設計候補

## 9. 禁止事項

- 競合記事にある項目をすべて追加する。
- 上位クエリを無条件で見出し化する。
- 検索ボリュームの低い周辺語を本文へ詰め込む。
- FAQを本文不足の代替にする。
- 文字数をCoverageの主要指標にする。
