# Consistency Audit Runtime Specification v1.0

## 1. 役割

Consistency Auditは、記事内部および改善案内部の論理的一貫性を検証する。

記事品質の最終評価ではなく、矛盾・不整合・残存表現を特定する内部監査である。

## 2. 監査対象

### 必須

- article_title
- seo_title
- introduction
- headings
- body
- faq
- summary

### 任意

- meta_description
- tables
- captions
- internal_links
- image_alt
- structured_data
- improvement_plan
- before_after_pairs

## 3. 内部出力

```json
{
  "consistency_audit": {
    "status": "review",
    "confidence": "high",
    "issues": [
      {
        "code": "CC_NUMERIC_CONTRADICTION",
        "severity": "high",
        "locations": ["introduction", "body"],
        "values": ["月200円", "月500円"],
        "message": "月額費用が記事内で一致していません。",
        "recommended_resolution": "根拠を確認し、正しい数値へ統一する。"
      }
    ],
    "checked_sections": [
      "seo_title",
      "article_title",
      "introduction",
      "headings",
      "body",
      "faq"
    ]
  }
}
```

この構造は内部保持用であり、SIMS_FEEDBACK_V2へ直接追加しない。

## 4. 監査順序

### Step 1：記事の中心命題を抽出

次を特定する。

- 記事が答える主質問
- 記事の最終結論
- 対象者
- 対象製品・サービス
- 対象年度
- 主要条件
- 主要数値

### Step 2：タイトルと結論

次を確認する。

- SEOタイトルが本文の結論を過大表現していないか
- 記事タイトルが対象範囲を正しく表しているか
- 年度表記が本文と一致しているか
- 「無料」「最安」「必ず」など強い表現が本文で裏付けられているか

### Step 3：導入と本文

次を確認する。

- 導入で約束した内容が本文に存在するか
- 導入の結論と本文の結論が一致するか
- 導入だけ最新版へ直し、本文に旧情報が残っていないか
- 読者対象や条件が途中で変わっていないか

### Step 4：見出しと直下本文

次を確認する。

- 見出しの問いに直下本文が答えているか
- 見出しが断定し、本文が否定していないか
- 見出しで示した数や項目数と本文が一致するか
- H2とH3の包含関係が自然か

### Step 5：本文内部

次を確認する。

- 数値
- 単位
- 年度
- 価格
- 商品名
- 機種名
- OS名
- 制度名
- 対応条件
- 手順順序
- 可否表現

### Step 6：FAQと本文

次を確認する。

- FAQの答えが本文と一致するか
- FAQだけ古い情報になっていないか
- FAQが本文にない新しい断定を追加していないか
- FAQの質問と回答が対応しているか

### Step 7：まとめ

次を確認する。

- まとめが本文の結論を正しく要約しているか
- 本文で条件付きだった内容を断定に変えていないか
- 新しい数値・情報をまとめで初出させていないか

### Step 8：改善案の整合性

次を確認する。

- Before/Afterの対象が一致しているか
- `changes`が実変更と一致しているか
- 修正後SEOタイトルと修正後本文の結論が一致しているか
- FAQ追加によって新しい矛盾が生じていないか
- 内部リンクの説明とリンク先テーマが一致しているか

## 5. 重大度

### critical

危険、法的誤認、健康被害、重大な制度誤認など、読者に深刻な損害を与える可能性がある。

### high

記事の中心結論、価格、年度、対応可否などが矛盾し、読者の判断を誤らせる。

### medium

一部条件、対象範囲、説明順序に矛盾があり、理解を妨げる。

### low

表記揺れ、軽微な名称差、句読点や書式の不統一。

## 6. status

- `pass`: 矛盾なし
- `pass_with_suggestions`: 軽微な揺れのみ
- `review`: medium以上の問題あり
- `fail`: criticalまたは重大なhigh問題あり

## 7. 禁止事項

- 表記揺れだけで全文改稿を提案する。
- 数値差を根拠確認せず多数決で統一する。
- FAQだけを本文と切り離して修正する。
- タイトルの表現に本文を無理に合わせる。
- 新しい情報へ更新した際に旧年度表現を残す。
- 推定値を確定値として統一する。
