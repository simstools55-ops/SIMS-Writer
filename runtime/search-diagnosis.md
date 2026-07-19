# Search Diagnosis Runtime Specification v1.0

## 1. 役割

Search Diagnosisは、Search Consoleデータから「何を直すか」ではなく、「なぜ現在の状態になっている可能性が高いか」を判定する内部処理である。

改善提案は、Search Diagnosisが完了した後に生成する。

## 2. 入力

### 必須

- main_query
- main_query_source
- article_rank
- article_clicks
- article_impressions
- article_ctr
- article_average_position

### 任意

- top_queries
- previous_period_metrics
- improvement_history
- article_age_days
- seasonal_context
- SERP features
- requested_priorities

不足した任意入力は推測で補完しない。

## 3. 内部出力

```json
{
  "search_diagnosis": {
    "primary_type": "CTR_OPPORTUNITY",
    "secondary_types": [],
    "confidence": "medium",
    "reason_codes": [
      "RC_POSITION_TOP10",
      "RC_CTR_BELOW_EXPECTED"
    ],
    "evidence": {
      "clicks": 12,
      "impressions": 1200,
      "ctr": 1.0,
      "average_position": 4.8
    },
    "recommended_action": "title_snippet_review",
    "do_not_change": [],
    "limitations": []
  }
}
```

この構造は内部保持用であり、SIMS_FEEDBACK_V2へ直接追加しない。

## 4. 診断順序

### Step 1：入力妥当性

次を確認する。

- 数値が欠落していないか
- CTRが0〜100の範囲か
- 平均順位が0より大きいか
- クリック数が表示回数を超えていないか
- main_queryとtop_queriesに重大な不一致がないか

重大な入力矛盾がある場合は、診断を停止して`DATA_INCONSISTENT`とする。

### Step 2：サンプル量

表示回数とクリック数から、判断に十分な量があるか確認する。

LOW_SAMPLEを優先判定した場合でも、明白な傾向があれば副診断として保持できる。ただしconfidenceは原則lowまたはmediumとする。

### Step 3：順位帯

平均順位を次の帯に分類する。

- 1.0〜3.0：TOP3
- 3.1〜5.0：TOP5
- 5.1〜10.0：PAGE1
- 10.1〜20.0：PAGE2
- 20.1〜50.0：LOW_VISIBILITY
- 50.1以降：VERY_LOW_VISIBILITY

### Step 4：CTR評価

CTRは順位帯とクエリ性質を考慮して評価する。

固定の全記事共通CTR基準だけで判定してはならない。

### Step 5：クエリ構成

top_queriesがある場合、次を確認する。

- main_queryの寄与率
- 上位クエリ間の検索意図の一致
- 異なる意図のクエリ流入
- 指名・非指名
- 情報収集・比較・購入検討の混在
- 主クエリだけ強く、記事全体CTRが低いケース

### Step 6：記事ランク

記事ランクは診断の補正に使う。

- S・A：過剰修正を避ける
- B：成長余地の診断を優先
- C：検索意図・構成・順位改善を重点確認
- D：記事全体の再設計候補

記事ランクだけで診断を決定しない。

### Step 7：主診断と副診断

主診断は1つに限定する。

副診断は最大2つまでとする。

例：

```text
Primary: POSITION_GAP
Secondary: CTR_OPPORTUNITY
```

平均順位18位でCTRが低い場合、主診断をCTR_OPPORTUNITYにしてはならない。

## 5. confidence

### high

- 十分な表示回数がある
- 数値に矛盾がない
- main_queryが明確
- top_queriesの傾向が主診断と一致
- 時系列がある場合、同じ傾向を確認できる

### medium

- データは利用可能だが、一部の入力がない
- 表示回数が中程度
- 複数原因が考えられる
- main_queryは明確だが、top_queriesが少ない

### low

- LOW_SAMPLE
- main_queryがestimated
- 数値矛盾がある
- 記事期間が短い
- 季節要因を除外できない
- top_queriesがなく原因を限定できない

## 6. 禁止事項

- CTRが低いという理由だけでSEOタイトルを変更する。
- 平均順位20位以下の記事へCTR改善を主提案する。
- 表示回数が少ない記事を重大問題と断定する。
- S・A記事を小さな数値変動だけで全面改稿する。
- 依頼文の改善優先順位を診断結果より優先する。
- main_queryと無関係な上位クエリを記事本文へ無理に追加する。
- 検索順位と記事品質を同一視する。
