# v0.2.3 から v1.0.0 への移行

1. リポジトリをv1.0.0一式で上書きする。
2. Claude Projectのファイルを`SIMS-Writer-Claude-v1.0.0-Baseline.zip`の内容へ差し替える。
3. 記事改善時に`batch_key`を指定する（最初は`BATCH-001`）。
4. 出力JSONの`swls`をLearning Recordとして保存する。
5. 利用者コメントと再測定値を各テンプレートへ記録する。
6. 10記事揃ったら`tools/swls_report.py`を実行する。
