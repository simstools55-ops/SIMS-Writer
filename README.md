# SIMS Writer Phase A6 — Regression Test Framework v1.0

## 目的

Phase A0〜A5で設計した品質パイプラインが、実際の記事改善で正しく機能するかを10記事の回帰テストで検証する。

Phase A6では新しい品質概念を追加しない。誤判定、過剰修正、修正不足、出力不整合を観測し、既存フェーズへフィードバックする。

```text
実記事入力
    ↓
A0〜A5で評価
    ↓
記事別テスト記録
    ↓
欠陥分類
    ↓
共通傾向分析
    ↓
修正対象Phase特定
    ↓
再テスト
    ↓
RC判定
```

## 検証対象

- Contract Validation
- Search Diagnosis
- Consistency Audit
- Evidence Audit
- Coverage Audit
- Preservation Score
- Change Budget
- Rewrite Level
- Rewrite Scope
- Risk Assessment
- Quality Gate
- SIMS_FEEDBACK_V2

## 収録ファイル

```text
runtime/
├─ regression-test-procedure.md
├─ article-evaluation-workflow.md
├─ defect-classification.md
└─ feedback-loop.md

templates/
├─ article-test-input-template.md
├─ article-evaluation-template.md
├─ defect-report-template.md
└─ ten-article-summary-template.md

tests/
└─ regression-acceptance-criteria.md
```

## テスト単位

1記事につき、次の2つを同じ形式で受領する。

1. SIMS-Blog-Managerの依頼文
2. SIMS Writerの回答

各記事を個別評価し、10記事終了時に累積分析を行う。

## 完了条件

- 10記事を同一基準で評価
- 全記事の判定根拠を記録
- 誤判定をPhase別に分類
- 過剰修正率・修正不足率を算出
- Blocking誤検出・見逃しを確認
- A0〜A5の修正要否を確定
- RC移行可否を判定


## v0.2.2 RC Hotfix

This release enforces V2 JSON, adds specialist validation, and replaces raw-HTML Before/After boxes with wrapping Markdown blockquotes. See `RELEASE_NOTES_v0.2.2_RC_HOTFIX.md`.
