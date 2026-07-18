# Improvement Strategy Engine v1.0

## 1. 役割

Phase A0〜A4の監査結果を統合し、最適な改善範囲を決定する。

## 2. 入力

- Quality Standard評価
- Contract Validation
- Search Diagnosis
- Consistency Audit
- Evidence Audit
- Coverage Audit
- article_rank
- current performance
- improvement_history
- requested_priorities

## 3. 内部出力

```json
{
  "improvement_strategy": {
    "decision": "targeted_revision",
    "preservation_score": 84,
    "change_budget_percent": 15,
    "rewrite_level": "L2",
    "rewrite_scope": "S3",
    "risk": "medium",
    "protected_elements": [
      "main_query focused title",
      "high-performing introduction"
    ],
    "change_targets": [
      "H2: 電気代の計算方法",
      "FAQ: 年間コスト"
    ],
    "rationale": [
      "Coverage不足は局所的",
      "検索順位は良好",
      "本文全体の一貫性は高い"
    ]
  }
}
```

## 4. decision

- `no_change`
- `minor_polish`
- `targeted_revision`
- `section_rebuild`
- `structural_rewrite`
- `full_rewrite_candidate`

## 5. 判定順序

1. blocking issueの有無
2. Preservation Score
3. Search Diagnosis
4. Consistency severity
5. Evidence Score
6. Coverage Score
7. Risk Assessment
8. Change Budget
9. Rewrite Level
10. Rewrite Scope

## 6. 基本判断

### no_change

- Preservation Score 90以上
- Search DiagnosisがHEALTHYまたはPROTECT_WINNER
- critical/high矛盾なし
- Evidence 90以上
- Coverage 90以上

### minor_polish

- 軽微な表記、可読性、FAQ調整
- Change Budget 5%以下
- L1中心

### targeted_revision

- 局所的なEvidenceまたはCoverage不足
- L2〜L3
- Scope S1〜S3

### section_rebuild

- 特定H2配下に大きな不足
- L3〜L4
- Scope S3

### structural_rewrite

- 複数H2、検索意図、構造に問題
- L4
- Scope S4〜S5

### full_rewrite_candidate

- 中心結論の崩壊
- Coverage 40未満
- 高重大度矛盾が複数
- Search DiagnosisがREBUILD_CANDIDATE
- Preservation Scoreが低い
- L5 / S5候補

Dランクだけでfull_rewrite_candidateにしない。

## 7. requested_prioritiesの扱い

依頼文の改善優先順位は参考情報である。

監査結果と矛盾する場合、Improvement Strategy Engineの判断を優先する。

## 8. 保護対象

変更前に次を明示する。

- 高CTRを支えるタイトル表現
- 上位クエリとの一致
- 独自体験
- 読者に役立つ具体例
- 既存の内部リンク導線
- 高品質な図表
- 検索意図へ直接答える結論

## 9. 禁止事項

- 数値スコアだけで全面改稿を決める。
- Preservation Scoreの高い記事をL4以上にする。
- Change Budgetを超える変更を無警告で実施する。
- 診断根拠なしにRewrite Scopeを広げる。
