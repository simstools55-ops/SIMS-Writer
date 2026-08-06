# SIMS Writer

既存記事を、検索意図・Search Console・SERP・根拠・既存価値の保全に基づいて改善する、SIMS Editorial Platformの治療専門製品です。

- Product Version: `3.3.0`
- Platform Compatibility: `SIMS Editorial Platform 1.x`
- Shared Version: `3.3.0`
- Repository Type: `Product`

## 責務

- SBMの日次改善依頼を処理する
- SBMがDoctor Referralから生成したWriter Treatment Requestを処理する
- 公開OK／利用者判断のBefore・Afterを生成する
- Winner Query、独自体験、広告・アフィリエイト要素などの保護対象を維持する
- Treatment ResultをSBMへ返す

Writerは診断Caseを管理せず、新記事作成や記事統合を直接実行しません。CreatorまたはMergeが適切な場合は、SBM向けFollow-up Referral候補を返します。

## Platform Contract

標準経路：

- `SIMS_WRITER_TREATMENT_REQUEST_V1`
- `SIMS_WRITER_TREATMENT_RESULT_V1`
- `SIMS_PUBLICATION_RESULT_V1`

既存運用との互換として、`SIMS_FEEDBACK_V2` Contract 2.1／3.0／4.2を継続サポートします。

## Repository境界

Claude Project用パッケージは別Repositoryの`SIMS-Writer-Claude`で管理します。Doctor実装・Doctor診断Runtimeは本Repositoryに含めません。

## Test

```bash
pytest -q tests/platform tests/publication-qa/test_official_regression_suite.py
```
