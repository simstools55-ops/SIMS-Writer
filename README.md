# SIMS Writer Phase A3 — Consistency Audit Standard v1.0

## 目的

記事の各構成要素を個別に評価するだけでなく、記事全体として結論・数値・年度・固有名詞・条件・回答が一致しているかを監査する。

```text
SEO title
Article title
Introduction
Headings
Body
FAQ
Summary
Internal links
        ↓
Consistency Audit
        ↓
Change Decision
        ↓
SIMS_FEEDBACK_V1
```

## 基本方針

- 表記揺れと意味矛盾を区別する。
- 記事の中心結論に影響する矛盾を優先する。
- 年度、価格、条件、対象機種など変動しやすい情報を重点確認する。
- 導入文だけ直して本文の古い表現を残さない。
- FAQを独立要素として扱わず、本文との回答一致を確認する。
- 外部出力はSIMS_FEEDBACK_V1 Version 1.2を維持する。

## 収録ファイル

```text
runtime/
├─ consistency-audit.md
├─ consistency-check-rules.md
└─ consistency-to-change-map.md

knowledge/
├─ contradiction-pattern-registry.md
└─ entity-consistency-rules.md

tests/
└─ consistency-regression-manifest.md
```

## 完了条件

1. 重大矛盾を見逃さない。
2. 表記揺れを重大矛盾として扱わない。
3. タイトル・導入・本文・FAQ間の結論を一致させる。
4. 年度・価格・製品名・数値の不一致を検出する。
5. 修正対象と`changes`フラグの矛盾を0件にする。
6. 外部JSON構造を変更しない。
