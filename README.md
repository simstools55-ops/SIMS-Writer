# SIMS Writer Phase A4 — Improvement Strategy Engine v1.0

## 目的

Phase A0〜A3の評価結果を利用し、記事を「直すべきか」「どこまで直すべきか」「どの範囲を守るべきか」を決定する。

```text
Quality Standard
Contract Validation
Search Diagnosis
Consistency Audit
        ↓
Evidence Audit
Coverage Audit
        ↓
Improvement Strategy Engine
        ├─ Preservation Score
        ├─ Change Budget
        ├─ Rewrite Level
        ├─ Rewrite Scope
        └─ Risk Assessment
        ↓
Quality Gate
        ↓
SIMS_FEEDBACK_V1
```

## 基本方針

- 良い記事ほど変更を抑える。
- 検索順位やCTRだけで全面改稿しない。
- 根拠不足と情報不足を区別する。
- 本文変更の深さと広さを分けて決定する。
- 変更量をChange Budgetで制御する。
- 高リスク変更はQuality Gateで再審査する。
- 外部出力はSIMS_FEEDBACK_V1 Version 1.2を維持する。

## 収録ファイル

```text
runtime/
├─ evidence-audit.md
├─ coverage-audit.md
├─ improvement-strategy-engine.md
├─ preservation-score.md
├─ change-budget-controller.md
├─ rewrite-level-and-scope.md
└─ risk-assessment.md

knowledge/
├─ evidence-level-registry.md
├─ coverage-pattern-library.md
└─ preservation-signal-registry.md

tests/
└─ improvement-strategy-regression-manifest.md
```

## 完了条件

1. 良好記事への過剰修正を抑止できる。
2. 根拠のない強い断定を検出できる。
3. 検索意図に必要な本文要素の欠落を判定できる。
4. Rewrite LevelとRewrite Scopeを分離できる。
5. Change Budgetを超える変更を警告できる。
6. 高リスク変更をQuality Gateへ引き渡せる。
7. SIMS_FEEDBACK_V1の外部構造を変更しない。
