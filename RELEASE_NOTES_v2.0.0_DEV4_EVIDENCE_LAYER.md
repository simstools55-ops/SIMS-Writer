# v2.0.0-dev.5 — Integrated Evidence Layer

- Search Console・verified SERP・一次/二次情報を統合するEvidence Layerを追加。
- HIGH/MEDIUM/LOW/NONEの内部Evidence判定をEditorial Decisionへ接続。
- LOWはUSER_DECISION、NONEはINTERNAL_REJECTへ固定。
- 未確認事実がPUBLIC_OKの別コンポーネントへ混入する矛盾をEVIDENCE-CONTAMINATION-001で遮断。
- GapをSUPPORTED_GAP / DECISION_GAP / UNSUPPORTED_GAP / NO_GAP / SEPARATE_INTENTへ分類。
- 利用者向けには内部スコアを出さず、必要な確認資料だけを提示。
- 冒頭に一行の平易な改善戦略を表示可能にした。
