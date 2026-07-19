# Consistency to Change Map v1.0

## 1. 原則

矛盾を見つけた箇所だけでなく、矛盾の発生源と影響範囲を確認して変更対象を決める。

## 2. 対応表

| 問題 | 主な修正対象 | 補助対象 |
|---|---|---|
| SEOタイトルと本文結論の不一致 | seo_title または body | introduction、description |
| 記事タイトルと対象範囲の不一致 | article_title | introduction、headings |
| 導入と本文の結論不一致 | introduction または body | summary、faq |
| 見出しと本文の不一致 | headings または body | faq |
| 数値の不一致 | 根拠確認後に該当箇所 | title、faq、table |
| 年度の不一致 | 全関連箇所 | description、faq |
| FAQと本文の不一致 | faq または body | summary |
| まとめと本文の不一致 | summary | introduction |
| 内部リンク説明の不一致 | internal_links | anchor text |
| 商品名・制度名の不一致 | 全出現箇所 | title、description |

## 3. changesフラグ

### introduction

最初のH2より前の本文を変更した場合のみtrue。

### headings

H2またはH3の文言・順序・階層を変更した場合true。

### body

最初のH2以降の本文段落を変更した場合true。

### faq

FAQの質問または回答を変更した場合true。

### seo_title

SEOタイトルを実際に変更した場合true。

### article_title

記事内H1またはCMS記事タイトルを変更した場合true。

### description

メタディスクリプションを変更した場合true。

### internal_links

リンク追加・削除・置換・アンカーテキスト変更を実施した場合true。

## 4. 変更範囲の決定

### 局所修正

- lowまたはmediumの問題
- 中心結論に影響しない
- 1〜2箇所で解消可能

### 複数箇所修正

- 同じ古い情報が導入・本文・FAQに残る
- 年度や数値が複数箇所で不一致
- タイトルと本文の両方を調整する必要がある

### 全体再設計候補

- 中心結論が複数存在
- 見出し構造と本文内容が広範囲で不一致
- 比較対象が途中で変わる
- 記事全体が異なる検索意図を混在させる

## 5. SIMS_FEEDBACK_V2への反映

Consistency Auditの内部問題は、次へ変換する。

- 実変更箇所 → `changes`
- 管理対象の新しい値 → `new_values`
- 重要な未解決問題 → `warnings`
- 修正概要 → `summary`
- 修正規模 → `improvement_type`
- 人間確認が必要 → `confidence`を調整
