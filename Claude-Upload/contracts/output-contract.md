# SIMS Feedback V2 — Contract 4.0

`format`名はSBM互換のため`SIMS_FEEDBACK_V2`を維持する。唯一の現行契約バージョンは`4.0`。

## 許可する最上位項目

- `format`
- `contract_version`
- `site_id`
- `site_name`
- `site_url`
- `article_id`
- `article_url`
- `completed_at`
- `publication_result`
- `recommended_review_days`
- `next_action`

## publication_result

- `change_summary`: 利用者向けの短い文字列配列
- `public_ok_changes`: そのまま反映できる変更
- `user_decision_changes`: 利用者確認が必要な変更

旧`changes`、`validation`、`publication_qa`、`swls`、`protected_elements`、`internal_link_evaluation`などは内部監査記録へ保存し、Contract 4.0 JSONへ出力しない。

## Gold Explainability Gate
- SERP比較件数・掲載数は実測値だけを表示する。未計測なら省略する。
- 各Gapに重要度1〜5と星表記を付ける。重要度は需要、SERP共通性、自記事不足、Evidenceで決める。
- SERP Gap Reportには3〜5行の利用者向けDecision Traceを付ける。
- USER_DECISIONには2〜5行のDecision Traceを付け、なぜ公開OKにしなかったかを平易に示す。
- 生の思考過程、内部スコア、競合URL一覧は表示しない。
