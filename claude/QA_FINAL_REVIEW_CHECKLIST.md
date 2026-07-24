# SIMS Writer Claude Final QA Checklist v1.0

改善案のBefore/Afterを作成した後、公開版を提示する前に必ず実行する。

1. 安全性・YMYLを確認する。
2. 数値、単位、月額・年額、割合を再計算する。
3. Query Coverage、Winner Query、Query Mix、LOW_SAMPLE判断を再確認する。
4. 体験談、独自情報、広告、比較表、画像を保護したか確認する。
5. 内部リンクの関連性・確認状態・実装状態を分離する。
6. SIMS_FEEDBACK_V2 Contractを正規化し、空文字を除去する。
7. Validationが本文とJSONの不整合を見逃していないか確認する。
8. 問題が局所的なら許可済みAuto-Fixを行い、再評価する。
9. 最終判定、公開可否、修正記録、残存警告を提示する。

公開停止条件が残る場合、完成版として提示してはならない。
