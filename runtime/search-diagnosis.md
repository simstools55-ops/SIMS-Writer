# Search Diagnosis v2.1

## 診断タイプ

- POSITION_OPPORTUNITY
- LOW_SAMPLE
- CTR_OPPORTUNITY
- CONTENT_GAP
- INTENT_MISMATCH
- STRONG_CURRENT_PERFORMANCE
- STABLE
- INPUT_INCOMPLETE
- UNKNOWN
- OTHER

## 基本規則

- 診断は配列で保持し、必要なら複数を併記する。
- CTRだけ、順位だけ、記事ランクだけで判断しない。
- 主クエリと記事全体の成績を分けて評価する。
- 表示回数が少ない場合は `LOW_SAMPLE` を追加し、効果を断定しない。
- `POSITION_OPPORTUNITY` は、概ね順位4〜13付近で表示機会があり、CTRまたは検索語との見え方に改善余地がある場合に使用する。本文が強ければSERP要素を先に直す。
- `INTENT_MISMATCH` は、検索語の中心概念がタイトル・導入・見出し・回答に欠落、または別概念へ置換されている場合に使用する。
- 高CTR・上位の記事は `STRONG_CURRENT_PERFORMANCE` として保護を優先する。
- 記事ランクDなどのラベルだけで全面改稿を決めない。
