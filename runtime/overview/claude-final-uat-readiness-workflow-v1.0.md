# Claude Final UAT Readiness Workflow v1.0

実記事UATセッションの証拠取り込み、初心者セットアップ実測の検証、一般利用者テスト開始判定を一括実行する。

```bash
python -m runtime.sims_writer_runtime.cli \
  --run-claude-uat-readiness ./uat-sessions/UAT-ID \
  --output ./uat-final-report
```

固定テストや未記入テンプレートだけでは `user_test_ready` にならない。
