# SIMS Shared Editorial Knowledge v1.3.7 — Contract Cleanup, Reviewer Precision, Japanese UX and Release Cleaner

- `changes[].target`を`component`へ統一
- 空文字と未変更項目の出力を抑止
- `auto_fixes`、`review_trace`、QA契約識別子を固定
- 内部リンク評価を候補単位で保持
- LOW/MEDIUM Coverage時の断定抑制を強化
- 利用者向け専門用語を日本語基本・初出のみ英語併記へ変更
- `.pytest_cache`、`__pycache__`等を除去するRelease Cleanerを追加
