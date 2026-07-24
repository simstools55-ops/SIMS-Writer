# SIMS Editorial QA Self-Review Runtime v1.1

## 目的

Writerの改善案を公開前に独立評価し、安全な範囲だけ修正して再評価する。将来はArticle Creatorからも同じQA契約を利用できる構造とする。

## 実行契約

- Contract: `SIMS_EDITORIAL_QA_V1`
- 最大再評価: 既定2回、上限3回
- 初回判定と最終判定を分離
- 全修正を`review_trace`へ記録
- 保護対象フィールドの変更はロールバック
- 未解消のRequired Fixは公開停止

## 責務境界

共通化可能:
- 判定語彙
- 実行ポリシー
- 修正履歴
- Release Gate
- Regression評価形式

Writer固有:
- 既存記事の保全
- Winner Query Preservation
- Before/After
- SBM Feedback Contract

Creator固有:
- 新規記事構成
- Evidence planning
- 新記事用HTML packaging

QAは本文をゼロから再生成しない。安全な局所修正で解消できない問題は作成担当へ戻す。
