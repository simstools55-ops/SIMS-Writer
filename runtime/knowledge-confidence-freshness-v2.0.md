# Knowledge Confidence and Freshness v2.0

## Purpose
公開OKは「情報が見つかった」だけでは決めない。出典階層、知識信頼度、最終確認日を統合して判定する。

## Evidence source hierarchy
1. OFFICIAL — 公式ヘルプ、公式仕様、公式告知
2. PRIMARY — 法令原文、研究原著、当事者一次資料
3. MULTIPLE_THIRD_PARTY — 独立した複数の信頼できる二次資料
4. SINGLE_THIRD_PARTY — 単独の二次資料
5. COMMUNITY — 掲示板、SNS、体験談
6. UNKNOWN — 出典不明

## Publication ceiling
- OFFICIAL / PRIMARY + current: PUBLIC_OK候補
- MULTIPLE_THIRD_PARTY: 原則USER_DECISION。公式確認なしで製品仕様を断定しない
- SINGLE_THIRD_PARTY / COMMUNITY: USER_DECISIONまたはINTERNAL_REJECT
- stale / contradicted / UNKNOWN: INTERNAL_REJECT

## Metadata
`source_level`, `verified_at`, `max_age_days`, `knowledge_confidence`, `contradicted` を内部監査に保持する。通常利用者にはスコアを表示しない。
