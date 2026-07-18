# Consistency Audit Regression Manifest v1.0

## 1. 目的

Consistency Auditが重大矛盾を検出し、軽微な表記揺れを過大評価しないことを確認する。

## 2. 必須テストケース

### CA-001 数値矛盾

入力：

```text
導入：月200円
本文：月500円
```

期待：

```text
CC_NUMERIC_CONTRADICTION
severity: high
status: review
```

### CA-002 条件付き数値

入力：

```text
通常は月200円前後
高性能機種では最大500円
```

期待：

```text
矛盾なし
```

### CA-003 年度残存

入力：

```text
SEOタイトル：2026年版
本文：2025年時点の制度
FAQ：2025年の回答
```

期待：

```text
CC_YEAR_CONTRADICTION
CC_STALE_CONTENT_REMAINS
```

### CA-004 可否矛盾

入力：

```text
本文：iPhoneでは利用できる
FAQ：iPhoneには非対応
```

期待：

```text
CC_AVAILABILITY_CONTRADICTION
severity: high
```

### CA-005 見出し不一致

入力：

```text
H2：無料で使う方法
本文：有料プランの契約手順のみ
```

期待：

```text
CC_HEADING_BODY_MISMATCH
```

### CA-006 表記揺れ

入力：

```text
Wi-Fi
WiFi
wifi
```

期待：

```text
CC_STYLE_VARIATION
severity: low
status: pass_with_suggestions
```

禁止：

```text
fail
full rewrite
```

### CA-007 FAQ追加による矛盾

入力：

本文では条件付き、追加FAQでは無条件に「必ずできる」と回答。

期待：

```text
CC_FAQ_BODY_MISMATCH
CC_CORE_CONCLUSION_CONTRADICTION
```

### CA-008 導入だけ更新

入力：

導入を2026年情報へ変更し、本文に旧価格が残る。

期待：

```text
CC_STALE_CONTENT_REMAINS
changes.introduction: true
changes.body: true
```

### CA-009 比較対象の混同

入力：

前半は商品AとBを比較し、後半で商品AとCの価格を比較。

期待：

```text
CC_COMPARISON_AXIS_DRIFT
CC_SCOPE_CONTRADICTION
```

### CA-010 Before/After不一致

入力：

BeforeはSEOタイトル、Afterは記事タイトル。

期待：

```text
CC_BEFORE_AFTER_MISMATCH
```

### CA-011 内部リンク説明不一致

入力：

「iPhone設定方法」と説明して、Androidの記事へリンク。

期待：

```text
CC_LINK_DESCRIPTION_MISMATCH
```

### CA-012 単位差

入力：

```text
月額200円
年間200円
```

期待：

```text
CC_UNIT_MISMATCH
severity: high
```

## 3. 既存記事テストへの適用

既存9記事のJSONと改善内容を用いて、次を確認する。

- 年度表記が全要素で一致するか
- changes.bodyと実変更箇所が一致するか
- FAQの回答が本文と一致するか
- main_queryとタイトル・導入の焦点が一致するか
- 内部リンク説明とリンク先が一致するか
- article_titleとseo_titleを混同していないか

## 4. 合格基準

- 必須12ケースの期待コード一致率100%
- critical/high矛盾の見逃し0件
- 表記揺れをfail判定するケース0件
- changesフラグ誤判定0件
- 年度更新時の旧情報残存見逃し0件
- SIMS_FEEDBACK_V1構造変更0件
