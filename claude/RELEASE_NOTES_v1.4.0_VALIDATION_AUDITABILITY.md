# v1.4.0 Validation Auditability

## Purpose
Validationを短く具体的な監査証跡へ整理し、SBM表示と機械処理の両方を安定化する。

## Changes
- Validation標準メッセージを40〜80文字程度へ簡潔化
- `protected_elements`・`changes`との重複列挙を削減
- `review_trace`を `cycle / checked[] / findings[] / actions[] / result` に固定
- `review_cycles_used`をTraceの最大cycleへ自動同期
- `auto_fixes[].target`を`component`へ正規化
- 旧`auto_fix_applied`を実行結果から除外

## Compatibility
SIMS_FEEDBACK_V2 / Contract 2.1は維持する。
