# SIMS Writer Learning System（SWLS）Beta

SWLSは、SIMS Writer v1.0.0の運用試験機能です。モデルを自動再学習させる機能ではありません。記事改善の判断、利用者の採用結果、再測定値を10記事単位で集計し、Project Instructions／Runtime／Knowledge／Contract／Pattern Library／Test Coverageの改善候補を作成します。

## 1記事ごとに保存する3ファイル

- `records/<ArticleID>.learning.json`：Claudeが最終JSON内の`swls`として生成した学習記録
- `feedback/<ArticleID>.feedback.json`：利用者の採用状況・評価・コメント
- `measurements/<ArticleID>.measurement.json`：改善前後のGSC指標（測定後に追加）

## 10記事レポート

同じ`batch_key`のLearning Recordが10件になったら、`tools/swls_report.py`で次を生成します。

- Markdown：人が読む総括
- JSON：機械処理用の集計
- CSV：Excel／Googleスプレッドシート分析用

```bash
python tools/swls_report.py   --records learning/records   --feedback learning/feedback   --measurements learning/measurements   --batch BATCH-001   --output learning/reports
```

## 改善候補の採用ルール

- 同種提案が3回以上発生した場合に「採用検討」とする。
- 1件だけの提案は即時に仕様へ反映しない。
- 利用者コメントだけで変更せず、Validation傾向や実測結果と合わせて判断する。
- v1.0.0 Baselineは固定し、採用変更はv1.0.xまたはv1.1.0で行う。
