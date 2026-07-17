# Batch Processing v1.0

SIMS Writerは、1つのフォルダに置いた複数の改善依頼JSONを順番に処理できます。

```bash
python -m runtime.sims_writer_runtime.cli \
  --batch-input examples/batch/requests \
  --output batch-output
```

各記事の成果物は`batch-output/items/<request-id>/`へ分離して保存されます。1件が失敗しても残りの処理を継続し、全体結果を`batch-summary.json`と`batch-summary.md`へ記録します。

CLI終了コードは全件処理できた場合が`0`、1件以上失敗した場合が`1`、入力フォルダ自体が不正な場合が`2`です。
