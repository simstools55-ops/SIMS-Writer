# Editorial QA Boundary v1.0

`SIMS_EDITORIAL_QA_V1`は製品中立の公開前QA契約である。

入力はRequest、Draft、Context、Policy。出力は初回判定、修正履歴、最終判定、公開可否、最終Draft。

QA Coreは記事を作成しない。Writer/Creator Adapterが各製品固有の入力をDraftへ変換し、結果を各製品Contractへ戻す。

当面の実装場所はSIMS Writerだが、共有可能な契約と評価語彙にWriter固有命名を持ち込まない。
