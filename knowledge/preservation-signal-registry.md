# Preservation Signal Registry v1.0

## PS_HIGH_RANK

上位表示を維持している。

## PS_HIGH_CTR

順位帯に対してCTRが良好。

## PS_MAIN_QUERY_ALIGNMENT

主クエリとタイトル・導入・本文が一致。

## PS_UNIQUE_EXPERIENCE

実体験や独自検証がある。

## PS_ORIGINAL_MEDIA

独自画像、図表、計算表がある。

## PS_STABLE_HISTORY

過去改善後に安定または上昇。

## PS_STRONG_INTERNAL_FLOW

内部リンク導線が自然。

## PS_CLEAR_CONCLUSION

検索意図への答えが明確。

## PS_HIGH_CONSISTENCY

記事内矛盾が少ない。

## PS_HIGH_EVIDENCE

確認可能性が高い。

## Negative Signals

- PN_INTENT_MISMATCH
- PN_STALE_INFORMATION
- PN_CORE_CONTRADICTION
- PN_LOW_COVERAGE
- PN_UNSUPPORTED_STRONG_CLAIM
- PN_DUPLICATE_CONTENT
- PN_LOW_VISIBILITY
- PN_WEAK_STRUCTURE


## v1.3.0 Hardening

Query Coverageは常時表示し、Primary／Secondary／Adjacent／Separate Articleへ分類する。Coverage Confidenceをhigh／medium／lowで示す。高CTR語句、完全一致クエリ、エラー文、固有名詞はWinner Query Preservation対象とする。複数意図が競合する場合はQUERY_MIXを検討する。warningは公開判断へ影響する事項に限定し、それ以外はinformationとする。
