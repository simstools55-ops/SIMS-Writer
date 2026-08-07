# SIMS_FEEDBACK_V2 Canonical Contract 2.1

最終出力の版数フィールドは`contract_version: "2.1"`とする。`version`、`diagnosis_code`、`change_flags`はNormalizer入力互換に限り、最終出力は禁止する。

変更は`changes[]`で表し、各要素に`target`、`implementation_status`、`before`、`after`、`reason`を持たせる。全体にも`implementation_status`を必須とする。

Query Coverageは`coverage_confidence`（high/medium/low）とPrimary、Secondary、Adjacent、Separate Articleの4分類を必須とする。

値のない任意項目は省略し、空文字を出力しない。warningsは公開判断へ影響する事項だけ、その他はinformationへ格納する。SchemaをSingle Source of Truthとする。
