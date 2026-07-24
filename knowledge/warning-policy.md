# Warning Policy v1.0

- W001 LOW_SAMPLE
- W002 SEASONAL_VARIATION
- W003 TREND_UNCERTAIN
- W004 E2_SUPPORT_LIMITED
- W005 STRONG_CLAIM_SOFTENED
- W006 CHANGE_BUDGET_EXCEEDED_MINOR
- W007 HIGH_RISK_CHANGE
- W008 RECENTLY_IMPROVED
- W009 QUERY_MIX_EFFECT
- W010 PROTECTED_ELEMENT_TOUCHED
- W011 COVERAGE_PARTIAL
- W012 DATA_INCONSISTENT_NONCRITICAL
- W013 CONFIDENCE_LOW
- W014 MANUAL_REVIEW_RECOMMENDED

利用者向けには内部コードをそのまま表示せず、行動につながる簡潔な日本語へ変換する。


## v1.3.0 Hardening

Query Coverageは常時表示し、Primary／Secondary／Adjacent／Separate Articleへ分類する。Coverage Confidenceをhigh／medium／lowで示す。高CTR語句、完全一致クエリ、エラー文、固有名詞はWinner Query Preservation対象とする。複数意図が競合する場合はQUERY_MIXを検討する。warningは公開判断へ影響する事項に限定し、それ以外はinformationとする。
