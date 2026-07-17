# Release Acceptance — v0.15.4-alpha.1

## Scope

- `確認事項`と`information`の重複排除
- 確認事項がない場合の見出し省略
- Primary / Secondary検索意図の明確化
- 根拠のない順位改善予測の抑止

## Acceptance Criteria

- Project InstructionsとKnowledge PackのVersionが`0.15.4-alpha.1`で一致する
- main_query推定とarticle_catalog不足は`information`に残る
- 同内容を利用者向け`確認事項`へ繰り返さない
- 未解決事項がない場合は`確認事項`を出力しない
- Secondary intentは明確な補助意図がある場合だけ付与する
- expected_effectは変更箇所に近い定性的効果だけを述べる
