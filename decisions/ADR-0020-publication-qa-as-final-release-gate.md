# ADR-0020: Publication QAを最終リリースゲートとする

## Status
Accepted

## Context
実記事試験では、改善判断が妥当でも、数値、内部リンク状態、Contract、Validationに局所的な不整合が残る例が確認された。

## Decision
Stage 9の品質検証、Stage 10の限定修正、Stage 11の公開パッケージ化をPublication QA Engineが統括する。初回評価、限定修正、再評価を経て、公開可能な最終版だけをパッケージ化する。

## Consequences
- 記事品質と機械連携品質を分離して検査できる
- 軽微な欠陥は利用者へ渡す前に修正できる
- 重大欠陥は公開停止できる
- QAが主要編集判断を上書きしない境界が必要になる
