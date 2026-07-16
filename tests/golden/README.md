# Golden Dataset

SIMS WriterのEnd-to-End品質を固定する回帰データセットです。各Caseは入力、Fixture Draft、期待するPublish Decision、必須・禁止要素を保持します。

## 実行

```bash
python tools/uat/run_golden_uat.py
```

Golden Caseは成功例だけでなく、入力不足、時点依存情報、高リスク主張、Placeholder修正を含みます。期待値を実行結果から自動更新する運用は禁止します。
