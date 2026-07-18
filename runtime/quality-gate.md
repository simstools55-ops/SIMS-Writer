# Quality Gate Runtime Specification v1.0

## 役割
Quality GateはSIMS Writerの唯一の出力許可層である。A0〜A4の結果を統合し、改善案の外部出力可否を決定する。

## 入力
- Contract Validation
- Search Diagnosis
- Consistency Audit
- Evidence Audit
- Coverage Audit
- Improvement Strategy
- Requested Output
- Runtime Context

## 処理順序
1. 入力完全性
2. Blocking Rule
3. Strategy整合性
4. Warning Policy
5. Confidence
6. Riskとの組み合わせ
7. Gate Decision Matrix
8. Quality Report
9. Runtime Health
10. 外部出力許可

## 最終出力例
```json
{
  "quality_gate": {
    "decision": "PASS_WITH_WARNING",
    "blocking_issues": [],
    "warnings": [{"code":"W_LOW_SAMPLE","message":"表示回数が少ないため診断確度が限定的です。"}],
    "confidence": "MEDIUM",
    "risk": "LOW",
    "output_allowed": true,
    "review_recommended": false
  }
}
```

## 判定
- PASS: Blocking/Warning/矛盾なし
- PASS_WITH_WARNING: Warningあり、出力可
- REVIEW_REQUIRED: 人間確認なしでは危険、出力不可
- BLOCK: 重大違反、出力不可

## output_allowed
- PASS: true
- PASS_WITH_WARNING: true
- REVIEW_REQUIRED: false
- BLOCK: false

## 禁止事項
- Quality Gateを省略した出力
- BlockingのWarning化
- スコアによるContract違反相殺
- REVIEW_REQUIREDの自動PASS化
