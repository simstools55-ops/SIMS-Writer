# SIMS Writer v1.3.8 Regression Hotfix

- 旧 `target` / `description` / `auto_fix_applied` 指示の競合を解消。
- `component` / `meta_description` / `auto_fixes` を最終正規形として強制。
- Validation空メッセージ、expected_effect空文字、未変更changesを最終正規化。
- `review_trace` と `unresolved_findings` を構造化配列へ統一。
- 未解決事項がある `PASS` を `PASS_WITH_WARNING` へ整合。
- 強い断定・主観・条件不明の数値一般化を公開前に停止。
- 利用者向け日本語語彙を追加。
- Release Cleanerを再検証。
