# Quality Validation Runtime v0.9.0-alpha.1

42件の正式Quality Ruleを読み込み、各Ruleを `pass` / `fail` / `warning` / `unable_to_verify` で評価します。決定論的に判定可能な規則は自動評価し、文脈判断が必要な規則は根拠なしに合格扱いせず、Model-Assisted Reviewerまたは人間レビューを要求します。

## 出力
- 全RuleのQuality Check
- 13 Dimension Score
- 7 Gate Result
- Severity別Issue
- Publish Recommendation
