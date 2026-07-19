# Feedback Loop v1.0

## 1. 目的

回帰テストで発見した欠陥を、最小の修正範囲でA0〜A5へ戻す。

## 2. 修正先の基本対応

| 欠陥 | 主な修正先 |
|---|---|
| 必須出力欠落 | A1 Contract |
| 検索診断誤り | A2 Search Diagnosis |
| 年度・数値矛盾 | A3 Consistency |
| 根拠判断誤り | A4 Evidence |
| 本文不足・過剰網羅 | A4 Coverage |
| 変更量誤り | A4 Strategy |
| 誤PASS・誤BLOCK | A5 Quality Gate |
| 英文思考混入 | Project Instructions / Runtime |
| JSON破損 | A1 / A5 |
| 記事タイプ固有問題 | Phase B候補として保留 |

## 3. 修正優先順位

1. CRITICAL
2. HIGH再発
3. SYSTEMIC
4. MEDIUM再発
5. LOW

## 4. 修正ルール

- 観測1件だけで大規模ルールを追加しない。
- 特定記事への例外処理を避ける。
- 既存合格記事を壊さない。
- 修正ごとに反証テストを追加する。
- Phase Bの問題をPhase Aへ無理に詰め込まない。

## 5. 修正パッケージ

修正時は次を含める。

```text
change/
├─ defect-summary.md
├─ root-cause.md
├─ files-changed.md
└─ expected-impact.md

tests/
├─ failing-case.md
├─ regression-cases.md
└─ acceptance.md
```

## 6. RC判定への反映

次の場合、RC移行不可。

- CRITICAL未解決
- HIGHのSYSTEMIC欠陥
- 誤BLOCK
- Blocking見逃し
- 全文欠落
- 内部思考混入
- SIMS_FEEDBACK_V2破損
- 過剰修正率が基準超過
