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
- Contract 4.2の`publication_result.serp_gap_report`と表示内容を一致させる。

## Gold Explainability Gate
- SERP比較件数・掲載数は実測値だけを表示する。未計測なら省略する。
- 各Gapに重要度1〜5と星表記を付ける。重要度は需要、SERP共通性、自記事不足、Evidenceで決める。
- SERP Gap Reportには3〜5行の利用者向けDecision Traceを付ける。
- USER_DECISIONには2〜5行のDecision Traceを付け、なぜ公開OKにしなかったかを平易に示す。
- 生の思考過程、内部スコア、競合URL一覧は表示しない。
