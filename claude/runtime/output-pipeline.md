# RC Final Canonical Output Pipeline

1. Editorial Strategyを内部作成する。
2. Evidence / Freshnessを修正単位で評価する。
3. Progressive Editingで編集可能な修正だけを作る。
4. Publication Decisionを確定する。
5. Evidence Contaminationを検査する。
6. Visibility Filterで内部情報を除去する。
7. UX Filterで公開可否の一文化、理由の短文化、内部リンク結果の一文化を行う。
8. Contract 4.0 Schemaを検証する。
9. 利用者向け本文と最後のJSONを出力する。

EvidenceとPublication DecisionをStrategyが上書きしてはいけない。UX Filterは編集内容や公開判定を変更せず、表示だけを簡潔にする。


## SERP Gap Report Gate
- SERPが修正判断に使われた場合、短い比較結果を公開OKの前に置く。
- 強み・不足・適用・非適用を、利用者向け平易表現で示す。
- 競合にあるだけの項目をGap扱いしない。
- 未確認の件数・掲載率・上位10件比較を捏造しない。
- Contract 4.1の`publication_result.serp_gap_report`と表示内容を一致させる。
