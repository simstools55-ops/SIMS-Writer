# Improvement Strategy Regression Manifest v1.0

## 1. 目的

良好記事を守り、問題記事だけに必要な範囲の変更を適用できることを確認する。

## 2. 必須テスト

### IS-001 高品質A記事

入力：

```text
rank: A
position: 4.2
ctr: 8.4%
coverage: 94
evidence: 93
consistency: pass
```

期待：

```text
Preservation: 90以上
Budget: 0〜5%
Level: L0〜L1
Scope: S0〜S1
Risk: low
```

禁止：

```text
L4/L5
title全面変更
```

### IS-002 高順位・低CTR

入力：

```text
position: 3.5
ctr: 1.2%
coverage: 92
evidence: 90
```

期待：

```text
decision: targeted_revision
Level: L2
Scope: S1〜S2
本文全面変更なし
```

### IS-003 低順位・Coverage不足

入力：

```text
position: 18
coverage: 62
evidence: 82
consistency: pass
```

期待：

```text
Level: L3
Scope: S3
Budget: 15〜30%
```

### IS-004 強い断定の根拠不足

入力：

```text
claim: 必ず半額
support: unsupported
coverage: 95
```

期待：

```text
Evidence issue
Level: L1〜L2
Scope: S1
断定緩和または根拠追加
```

禁止：

```text
全文改稿
```

### IS-005 年度残存

入力：

```text
title: 2026年版
body: 2025年価格
faq: 2025年条件
```

期待：

```text
Level: L3
Scope: S3〜S4
Risk: medium
```

### IS-006 Dランクだが局所問題

入力：

```text
rank: D
coverage: 82
consistency: pass
evidence: 88
```

期待：

```text
full rewriteにしない
L2〜L3
```

### IS-007 Dランク＋意図崩壊

入力：

```text
rank: D
search diagnosis: REBUILD_CANDIDATE
coverage: 32
consistency: fail
preservation: 25
```

期待：

```text
decision: full_rewrite_candidate
Level: L5
Scope: S5
Risk: high
```

### IS-008 LOW_SAMPLE

入力：

```text
impressions: 35
diagnosis: LOW_SAMPLE
```

期待：

```text
decision: no_change or minor_polish
Level: L0〜L1
Risk: low
```

禁止：

```text
L4/L5
```

### IS-009 改善直後

入力：

```text
rank: B
days_since_improvement: 10
coverage: 80
```

期待：

```text
Budgetを減額
Riskを1段階引き上げる可能性
monitor優先
```

### IS-010 独自体験の保護

入力：

独自検証、実測値、画像がある。

期待：

```text
protected_elementsへ登録
AI的な一般文への置換禁止
```

### IS-011 Change Budget超過

入力：

```text
budget: 15%
planned_change: 45%
```

期待：

```text
risk: high
Quality Gate再審査
変更範囲縮小
```

### IS-012 不自然なLevel/Scope

入力：

```text
Level: L1
Scope: S5
```

期待：

```text
Semantic warning
再計算
```

### IS-013 E3未確認

入力：

医療・法律・金融の中心主張が未確認。

期待：

```text
blocking issue
Quality Gate停止候補
```

### IS-014 主クエリ良好記事

入力：

記事全体CTRは低いが、main_query CTRは高い。

期待：

```text
QUERY_MIX_EFFECTを考慮
タイトル変更抑制
Preservation加点
```

## 3. 合格基準

- 必須14ケース一致率100%
- 高品質記事のL4/L5誤判定0件
- LOW_SAMPLEの全面改稿0件
- E3未確認の見逃し0件
- Change Budget超過の無警告0件
- 独自体験の削除提案0件
- 不自然なLevel/Scopeの見逃し0件
- SIMS_FEEDBACK_V1構造変更0件
