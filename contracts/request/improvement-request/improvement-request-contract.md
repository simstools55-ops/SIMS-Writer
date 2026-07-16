# Improvement Request Contract v1.0

SIMS Writerが受け取る記事改善依頼の正規形を定義する。

- SIMS-Blog-Manager形式と汎用JSON形式を同一の正規形へ変換する。
- `schema_version` は Product 1.0 Implementation Phase では `1.0` 固定。
- `request_id`、`main_query`、`improvement_goal`、`requested_output` は必須。
- 入力不備は黙って補完せず、検証エラーとして明示する。
- 読込後の正規形はArticle Context生成とRuntime実行の共通入力とする。
