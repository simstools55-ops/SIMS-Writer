# Quality Foundation v1.0

## Execution order
1. Input completeness evaluation
2. Search performance diagnosis
3. Draft generation
4. Consistency audit
5. Contract validation
6. Targeted regeneration when blocking issues remain
7. Final JSON validation

## Gate status
- `pass`: blocking issueなし、warningなし。
- `pass_with_warnings`: 実行可能だが確認事項あり。
- `fail`: 数値矛盾、タイトル・本文不一致、FAQ不一致、Contract違反など公開前修正が必要。

## Blocking examples
- タイトルの時間・件数・価格が本文の範囲と矛盾する。
- FAQの回答が質問または本文と矛盾する。
- 実施変更とchange flagが一致しない。
- graceful degradationなのにestimated_fieldsが空。
- SEOタイトルを変更したのにnext_actionがmonitor。
