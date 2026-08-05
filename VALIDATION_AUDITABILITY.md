# Validation Auditability v1.4.0

## Message standard
- 空欄は禁止
- 40〜80文字程度を目安にする
- `protected_elements`や`changes`の全項目を再列挙しない
- 「何を照合したか」と「判定理由」を一文で示す

## Review trace
```json
{
  "cycle": 1,
  "checked": ["winner_query", "numeric_consistency", "causal_claims"],
  "findings": ["未確認の断定表現を1件検出"],
  "actions": ["meta_descriptionを中立表現へ修正"],
  "result": "PASS_WITH_WARNING"
}
```

自由文の`focus`だけで記録せず、`checked[]`を必須とする。
