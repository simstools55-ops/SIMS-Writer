# Publication QA Regression Validation

1. 固定入力と元回答は登録後に変更しない。
2. 各ケースは期待初回判定、必須検出事項、許可Auto-Fix、期待最終判定を持つ。
3. 原文未登録ケースはFAILではなくSKIPとし、正式回帰合格数には含めない。
4. 新バージョンは全READYケースを実行し、前版との差分を記録する。
