# Search Diagnosis Regression Manifest v1.0

## 1. 目的

Search Diagnosisが単純なCTR反応へ戻らないことを確認する。

## 2. 必須テストケース

### SD-001 高順位・低CTR

入力：

```text
impressions: 2000
clicks: 24
ctr: 1.2%
position: 3.5
rank: B
```

期待：

```text
Primary: CTR_OPPORTUNITY
confidence: high or medium
```

禁止：

```text
Primary: POSITION_GAP
```

### SD-002 低順位・低CTR

入力：

```text
impressions: 1500
clicks: 8
ctr: 0.53%
position: 18.0
rank: C
```

期待：

```text
Primary: POSITION_GAP
Secondary: CTR_OPPORTUNITY allowed
```

禁止：

```text
タイトル変更だけを主改善にする
```

### SD-003 少数データ

入力：

```text
impressions: 35
clicks: 0
ctr: 0%
position: 8.0
```

期待：

```text
Primary: LOW_SAMPLE
confidence: low
next_action: monitor
```

### SD-004 良好記事

入力：

```text
impressions: 5000
clicks: 420
ctr: 8.4%
position: 4.2
rank: A
```

期待：

```text
Primary: PROTECT_WINNER or HEALTHY
```

禁止：

```text
SEOタイトル全面変更
本文全面改稿
```

### SD-005 主クエリ良好・全体CTR低位

入力：

```text
article_ctr: 1.0%
main_query_ctr: 18%
main_query_position: 2.8
other_queries: low relevance
```

期待：

```text
Primary: QUERY_MIX_EFFECT
```

禁止：

```text
タイトルが弱いと断定
```

### SD-006 意図分散

入力：

複数の上位クエリが、使い方・料金・解約など別意図に分散。

期待：

```text
Primary: INTENT_FRAGMENTATION
```

### SD-007 比較期間なし

入力：

現在値だけがあり「最近下がった」と依頼文に書かれている。

期待：

```text
TREND_DECLINEを使わない
```

### SD-008 季節記事

入力：

年末年始・季節イベントに依存し、現在表示が減少。

期待：

```text
SEASONAL_VARIATION
confidence: medium以下
```

### SD-009 データ矛盾

入力：

```text
clicks: 120
impressions: 100
ctr: 120%
```

期待：

```text
Primary: DATA_INCONSISTENT
diagnosis stopped
```

### SD-010 Dランク記事

入力：

```text
rank: D
position: 38
ctr: 0.1%
impressions: 3000
intent mismatch confirmed
```

期待：

```text
Primary: REBUILD_CANDIDATE
next_action: rewrite
```

Dランクだけを理由にREBUILD_CANDIDATEにしない。

## 3. 既存9記事JSONへの追加監査

既存の9記事について、次を再判定する。

- CTR低位がタイトル問題として過剰診断されていないか
- 低順位記事でPOSITION_GAPが優先されるか
- main_query単位と記事全体の差を確認しているか
- estimated main_queryのconfidenceが過大でないか
- article_rankに応じて変更範囲が調整されているか

## 4. 合格基準

- 必須10ケースの主診断一致率100%
- 禁止判定0件
- LOW_SAMPLEの見逃し0件
- 高順位・低CTRと低順位・低CTRの混同0件
- 良好記事の過剰修正0件
- SIMS_FEEDBACK_V1の構造変更0件
