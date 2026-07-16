# Targeted Refinement Runtime v1.0

Quality IssueをRule ID・対象Component・原因Stageへ振り分け、安全な決定論的修正を先行して実行する。事実、検索意図、専門判断は自動補完せず、対象Stageへ戻すAction PlanまたはManual Reviewとして明示する。

## 初期自動修正

- Placeholder除去
- AI定型表現の削減
- 重複文の削減
- 見出し階層の補正

## 修正上限

自動修正は最大3回。品質問題が残る場合は対象Stageへ戻し、全文再生成を既定動作にしない。
