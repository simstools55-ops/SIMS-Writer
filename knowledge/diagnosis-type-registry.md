# Search Diagnosis Type Registry v1.0

## DATA_INCONSISTENT

Search Console入力値または依頼データに重大な矛盾がある。

例：

- clicks > impressions
- CTRが100%を超える
- 平均順位が0以下
- 集計期間が不明で比較不能

## LOW_SAMPLE

判断に必要なデータ量が不足している。

検索意図やタイトル問題を断定しない。

## CTR_OPPORTUNITY

十分な露出と比較的良い順位があるが、CTRが順位帯に対して弱い可能性がある。

「タイトルが悪い」と同義ではない。

## POSITION_GAP

検索結果への露出はあるが、主なクエリで上位表示へ届いていない。

本文、構成、検索意図、競合差を確認する。

## LOW_VISIBILITY

平均順位が低く、CTR評価よりも先に露出・関連性を確認すべき状態。

## INTENT_MISMATCH

main_queryが求める回答と、記事の主題・結論・構成がずれている。

## INTENT_FRAGMENTATION

異なる検索意図のクエリが同一記事へ流入し、記事の焦点が分散している可能性がある。

## QUERY_MIX_EFFECT

記事全体CTRの低さが、関連性の弱いクエリ表示や複数クエリ群によって生じている。

主クエリCTRが良好な場合に重要。

## TREND_DECLINE

過去期間と比べ、クリック、CTR、順位などが継続的に悪化している。

比較データなしでは使用しない。

## SEASONAL_VARIATION

季節、年度、イベント、需要期などによる自然変動の可能性が高い。

## HEALTHY

現状の検索パフォーマンスに重大な問題が見られず、積極的な修正を必要としない。

## PROTECT_WINNER

S・Aランクなど成果が出ている記事で、既存の強みを守ることが最優先。

## REBUILD_CANDIDATE

低順位・低CTR・意図不一致・構造問題が重なり、部分修正より全体再設計が合理的な可能性が高い。

## 使用制約

- Primaryは必ず1つ。
- Secondaryは最大2つ。
- TREND_DECLINEは比較期間がある場合のみ。
- SEASONAL_VARIATIONは季節根拠がある場合のみ。
- REBUILD_CANDIDATEはDランクだけで自動付与しない。
