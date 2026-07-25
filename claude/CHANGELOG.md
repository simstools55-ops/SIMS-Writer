# v1.3.9

- Validation Message Integrity Hotfix。空メッセージを正例・Schema・Normalizer・最終ゲート・テストの全層で禁止。

## 1.3.8 - Regression Hotfix

# SIMS Writer Claude v1.3.8 Regression Hotfix

旧出力指示との競合を除去し、Canonical Contract、日本語表示、Reviewer停止条件を最終強制しました。

# 1.3.7

# SIMS Writer v1.3.7 — Contract Cleanup, Reviewer Precision, Japanese UX and Release Cleaner

- `changes[].target`を`component`へ統一
- 空文字と未変更項目の出力を抑止
- `auto_fixes`、`review_trace`、QA契約識別子を固定
- 内部リンク評価を候補単位で保持
- LOW/MEDIUM Coverage時の断定抑制を強化
- 利用者向け専門用語を日本語基本・初出のみ英語併記へ変更
- `.pytest_cache`、`__pycache__`等を除去するRelease Cleanerを追加

# 1.3.6
- Locked Publication QA pipeline and canonical final output.

# 1.3.0 - Quality & Validation Hardening

- Writer本体v1.3.0と完全同期
- Shared Snapshot v1.3.0
- Contract 2.1運用指示を追加

# Changelog

## 1.1.1 - 2026-07-22
- Shared Editorial Knowledge v1.1.1へ同期。
- 中心主張優先検証、Source-Scope表現、LOW_SAMPLE時の最小変更を強化。
- 内部リンクのadopted / pending / rejected判定を明確化。

## 1.1.0 - 2026-07-21
- Production baseline.

## 1.3.2 - Publication QA Foundation

- Added mandatory final Publication QA workflow and safe auto-fix boundaries.
- Added five-level publication verdicts and release gate documentation.

## 1.3.3 - Regression Evaluation Profiles

- Added formal Publication QA evaluation standard.
- Added five Official Regression Suite case profiles and expected findings.
- Added regression readiness runner and QA checklist integration.
- Source article fixtures remain pending and are reported as SKIP.

## 1.3.4
- Added Self QA runtime instructions and platform-neutral QA contract reference.

## 1.3.5
- Added QA-reviewed final output integration rules.
