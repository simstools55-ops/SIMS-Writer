# Validation Rules v1.0

| Rule ID | 検査内容 | Severity | 失敗時 |
|---|---|---|---|
| VAL-001 | ArticleID一致 | BLOCKER | FAIL |
| VAL-002 | URL一致 | BLOCKER | FAIL |
| VAL-003 | Primary Intent維持 | BLOCKER | FAIL |
| VAL-004 | 保護対象維持 | BLOCKER | FAIL |
| VAL-005 | Change Budget内 | BLOCKER | FAIL |
| VAL-006 | Rewrite Level/Scope整合 | MAJOR | FAIL |
| VAL-007 | SEOタイトル45文字以内 | MINOR | WARNING |
| VAL-008 | メタディスクリプション80〜140文字 | MINOR | WARNING |
| VAL-009 | Before/After一対一対応 | MAJOR | FAIL |
| VAL-010 | FAQが本文重複でない | MINOR | WARNING |
| VAL-011 | 事実・数値の根拠 | BLOCKER | FAIL/UNVERIFIABLE |
| VAL-012 | 変更フラグと実出力一致 | MAJOR | FAIL |
| VAL-013 | JSON Schema v2.0適合 | BLOCKER | FAIL |
| VAL-014 | 英文分析・内部思考なし | BLOCKER | FAIL |
| VAL-015 | LOW_SAMPLE警告と再測定 | MAJOR | FAIL |
| VAL-016 | 出力の冒頭・末尾省略なし | MAJOR | FAIL |
