# SIMS Feedback Contract 4.2

`format`は後方互換のため`SIMS_FEEDBACK_V2`を維持する。正本は`publication_result`である。

利用者・SBMへ渡す項目は、サイト・記事識別情報、`publication_result`、`recommended_review_days`、`next_action`に限定する。

`publication_result.serp_gap_report`は、SERPを実際に確認し、修正判断の根拠になった場合だけ出力できる。内容は利用者が理解できる比較要約に限定し、内部スコア、Evidence階層、監査ログは含めない。比較件数や掲載率は実測できた場合だけ記録し、推測値を作らない。

診断、SERP生データ、Evidence、Knowledge Confidence、Freshness、Strategy、Progressive trace、SWLS、Validation、QA、保護要素、不採用候補は内部監査記録へ保存する。

## Gold Explainability Gate
- SERP比較件数・掲載数は実測値だけを表示する。未計測なら省略する。
- 各Gapに重要度1〜5と星表記を付ける。重要度は需要、SERP共通性、自記事不足、Evidenceで決める。
- SERP Gap Reportには3〜5行の利用者向けDecision Traceを付ける。
- USER_DECISIONには2〜5行のDecision Traceを付け、なぜ公開OKにしなかったかを平易に示す。
- 生の思考過程、内部スコア、競合URL一覧は表示しない。
