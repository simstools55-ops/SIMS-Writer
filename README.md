# SIMS Writer Phase A2 — Search Diagnosis Standard v1.0

## 目的

Search Consoleデータを直接改善案へ結び付けず、必ず原因診断を経由してから改善方針を決定する。

```text
Search Console data
        ↓
Search Diagnosis
        ↓
Improvement Decision
        ↓
SIMS_FEEDBACK_V1
```

## 基本方針

- CTRが低いだけでタイトル変更を決めない。
- 平均順位、表示回数、クリック数、クエリ構成、記事ランクを併せて判断する。
- データ不足時は無理に改善理由を断定しない。
- 記事内容の監査結果と検索データの診断結果を混同しない。
- 診断は内部契約として保持し、外部出力はSIMS_FEEDBACK_V1 Version 1.2を維持する。

## 収録ファイル

```text
runtime/
├─ search-diagnosis.md
├─ diagnosis-decision-table.md
└─ diagnosis-to-improvement-map.md

knowledge/
├─ diagnosis-type-registry.md
└─ search-console-interpretation-rules.md

tests/
└─ search-diagnosis-regression-manifest.md
```

## 完了条件

1. 低CTRを自動的にタイトル問題と断定しない。
2. 低順位時にCTR改善だけを提案しない。
3. 少数データをLOW_SAMPLEとして識別する。
4. 良好記事への過剰修正を抑止する。
5. 診断理由と改善対象の矛盾を0件にする。
6. 既存JSONの外部契約を変更しない。
