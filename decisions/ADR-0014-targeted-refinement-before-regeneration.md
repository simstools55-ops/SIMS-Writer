# ADR-0014 Targeted Refinement Before Regeneration

## Decision

Quality Fail時は、全文再生成より先にIssue Routerで原因と対象Componentを特定し、安全な修正のみ自動適用する。事実・検索意図・安全性の判断は自動創作せず、元StageまたはManual Reviewへ戻す。

## Consequences

追加編集量と既存価値の消失を抑え、修正履歴と再検証結果を追跡できる。
