# ADR-0013 Executable Quality Rules with Explicit Unverifiable State

## Decision
全42 Quality RuleをRuntimeで必ず実行する。決定論的に評価できない規則は推測でPassにせず `unable_to_verify` とし、Model-Assisted Reviewerまたは人間レビューの根拠を要求する。

## Rationale
品質の未確認を成功として隠さず、Publish Ready判定の信頼性を守るため。
