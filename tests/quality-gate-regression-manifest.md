# Quality Gate Regression Manifest v1.0

## 必須22ケース
1. 完全PASS → PASS
2. Warningあり → PASS_WITH_WARNING
3. ArticleID不一致 → BLOCK/B001
4. URL不一致 → BLOCK/B002
5. E3重大未確認 → BLOCK/B007
6. LOW Confidence + HIGH Risk → REVIEW_REQUIRED
7. LOW_SAMPLE + L5 → REVIEW_REQUIRED
8. Preservation 92 + L4/S4 → REVIEW_REQUIRED
9. Budget軽度超過 → PASS_WITH_WARNING/W006
10. Budget大幅超過 → REVIEW_REQUIRED
11. Before/After対象不一致 → BLOCK/B006
12. QUERY_MIX_EFFECT → タイトル全面変更なし
13. 改善後10日 + L4 → REVIEW_REQUIRED/W008
14. critical矛盾未解消 → BLOCK/B008
15. 出力JSON破損 → BLOCK/B009
16. 必須フェーズ欠落 → BLOCK/B012
17. Warning複数・整合あり → PASS_WITH_WARNING
18. HIGH Riskだが根拠十分 → 自動BLOCK禁止
19. no_change + changesあり → REVIEW_REQUIRED
20. Quality Reportに必須フェーズ・rule_trace
21. Runtime Health HEALTHY
22. Runtime Health UNHEALTHY

## 合格基準
- 22ケース一致率100%
- Blocking見逃し0件
- Blockingのスコア相殺0件
- LOW_SAMPLEの自動全面改稿0件
- LOW Confidence + HIGH Riskの自動PASS 0件
- ArticleID/URL不一致の出力許可0件
- 必須フェーズ欠落の出力許可0件
- SIMS_FEEDBACK_V2 Version変更0件
- Quality Gate未経由出力0件
