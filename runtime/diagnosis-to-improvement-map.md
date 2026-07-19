# Diagnosis to Improvement Map v1.0

## 1. 原則

診断タイプと改善対象を直接1対1に固定しない。

改善対象は、本文監査・タイトル監査・検索意図監査を経て確定する。

ただし、診断ごとの優先確認対象を定義する。

## 2. 対応表

| Diagnosis | 優先確認 | 変更候補 | 原則変更しない |
|---|---|---|---|
| LOW_SAMPLE | データ期間、記事公開日 | なし | 全面改稿 |
| DATA_INCONSISTENT | GSC入力、集計期間 | なし | すべて |
| CTR_OPPORTUNITY | SEOタイトル、記事タイトル、導入、スニペット | title、description、introduction | 本文全面改稿 |
| POSITION_GAP | 検索意図、見出し、本文網羅性 | headings、body、faq、internal_links | タイトルだけの修正 |
| LOW_VISIBILITY | 記事テーマ、競合、インデックス、意図 | body、headings、rewrite候補 | CTRのみの微調整 |
| INTENT_MISMATCH | main_queryと結論・構成 | title、introduction、headings、body | FAQだけの修正 |
| INTENT_FRAGMENTATION | 上位クエリ群、記事焦点 | headings、body、別記事候補 | 無関係クエリ追加 |
| QUERY_MIX_EFFECT | クエリ別CTR | 必要箇所のみ | タイトル問題の断定 |
| TREND_DECLINE | 前期間差、SERP変化、鮮度 | year、title、body | 原因未確認の全面改稿 |
| SEASONAL_VARIATION | 月別傾向、需要期 | 年度・季節表現 | 恒久的な問題の断定 |
| HEALTHY | 重大矛盾だけ確認 | 原則なし | 不要なリライト |
| PROTECT_WINNER | 維持すべき要素 | 局所修正のみ | タイトル・本文全面変更 |
| REBUILD_CANDIDATE | 意図、構成、正確性 | full候補 | 小手先だけの修正 |

## 3. SIMS_FEEDBACK_V2への反映

内部診断は、次の外部項目へ変換する。

### improvement_type

- LOW_SAMPLE / HEALTHY / PROTECT_WINNER：`minor`
- CTR_OPPORTUNITY / POSITION_GAP / TREND_DECLINE：原則`normal`
- INTENT_MISMATCH / REBUILD_CANDIDATE：`major`候補

最終的には変更範囲を見て再判定する。

### next_action

- LOW_SAMPLE：`monitor`
- DATA_INCONSISTENT：`none`または再取得をsummaryで指示
- CTR_OPPORTUNITY：`remeasure`
- POSITION_GAP：`remeasure`
- HEALTHY：`monitor`
- PROTECT_WINNER：`monitor`
- REBUILD_CANDIDATE：`rewrite`

### recommended_review_days

- タイトル・導入中心：14
- 本文・構成変更：30
- サンプル不足：30
- 明確な短期確認目的：7

## 4. changesとの整合性

- CTR_OPPORTUNITYで`body:true`にする場合、本文監査による別根拠が必要。
- POSITION_GAPで`seo_title:true`だけの場合、Semantic Validatorで警告する。
- LOW_SAMPLEで複数項目をtrueにする場合、検索データ以外の明確な問題を記録する。
- PROTECT_WINNERで`body:true`または`seo_title:true`の場合、変更理由をsummaryへ明記する。
