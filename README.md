# SIMS Writer Phase A5 — Quality Gate v1.0

## 目的
Phase A0〜A4の結果を統合し、改善案を利用者へ返してよいかを最終判定する。

A5自身は記事品質を新たに評価せず、各フェーズの監査結果を統合する唯一の出口として動作する。

## 最終判定
- `PASS`
- `PASS_WITH_WARNING`
- `REVIEW_REQUIRED`
- `BLOCK`

## 基本原則
- Blocking Ruleはスコアで相殺しない。
- データ不足と記事品質不足を区別する。
- HIGH RiskとLOW Confidenceの組み合わせは人間確認へ送る。
- LOW_SAMPLEを理由に全面改稿しない。
- 外部JSONは`SIMS_FEEDBACK_V1 Version 1.2`を維持する。

## 収録ファイル
```text
runtime/
├─ quality-gate.md
├─ gate-rules.md
├─ quality-report.md
├─ runtime-health.md
└─ gate-decision-matrix.md

knowledge/
├─ blocking-rule-registry.md
├─ warning-policy.md
├─ confidence-model.md
└─ quality-thresholds.md

tests/
└─ quality-gate-regression-manifest.md
```
