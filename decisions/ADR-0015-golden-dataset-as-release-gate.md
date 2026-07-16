# ADR-0015 Golden Dataset as Release Gate

- Status: Accepted
- Date: 2026-07-17

## Decision

実記事に近い固定CaseをGolden Datasetとして管理し、期待するPublish Decision、必須要素、禁止要素をリリース判定に使用する。期待値を実行結果から自動更新しない。

## Rationale

単体資産の整合だけでは、Knowledge・Decision・Pattern・Quality・Refinementを接続した際の品質退行を検出できないため。
