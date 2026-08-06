# Validation Auditability v1.4.0

Validationは空欄を避けるだけでなく、短く具体的な監査証跡として記録する。

- messageは40〜80文字程度を目安にする。
- `changes`や`protected_elements`を全文再掲しない。
- 照合対象と判定理由を一文で示す。
- `review_trace`は`cycle`、`checked[]`、`result`を必須とする。
- 必要な場合のみ`findings[]`と`actions[]`を追加する。
- `review_cycles_used`は最大cycle番号と一致させる。
