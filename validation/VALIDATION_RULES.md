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


## v1.1.0追加ルール

| Rule ID | 検査内容 | Severity | 失敗時 |
|---|---|---|---|
| VAL-017 | 検索文脈を識別するSERPエンティティを不用意に削除していない | MAJOR | FAIL/WARNING |
| VAL-018 | Hidden Anxietyが根拠・未回答・判断影響の条件を満たす | MINOR | WARNING |
| VAL-019 | FAQが本文読後の残存疑問を解決し、本文と過度に重複しない | MINOR | WARNING |
| VAL-020 | 内部リンク採用が意味的補完性と確認済みURLを満たす | MAJOR | FAIL |
| VAL-021 | 断定表現がEvidence分類の強さを超えていない | MAJOR | FAIL/WARNING |
| VAL-022 | 条件付き結論が既存根拠に基づき、体験を創作していない | BLOCKER | FAIL |
| VAL-023 | 入力されたSiteID/SiteName/SiteURL/ArticleID/ArticleURLを透過保持する | MAJOR | FAIL |
