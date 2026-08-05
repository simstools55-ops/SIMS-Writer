
## v3.1.0 Revenue First Validation

Revenue impact, search intent, winner-query preservation and publication integrity now determine blocking priority. Editorial polish with negligible SEO impact remains non-blocking.
# SIMS Shared Editorial Knowledge v3.2.0

# SIMS Shared Editorial Knowledge

SIMS WriterとSIMS Article Creatorが共有する編集品質基準の正本（Single Source of Truth）です。

## 目的

- 両製品で共通するSEO・編集・Evidence知識を一元管理する
- 共通知識と製品固有の適用ルールを分離する
- WriterのPreservation思想とCreatorの新規設計思想を混同しない

## 構成

```text
knowledge/                 共通知識の正本
strategy/                  編集戦略
evidence/                  出典・公開境界
patterns/                  再利用可能な編集パターン
quality/                   Quality Pattern Libraryと品質契約
mappings/writer/           Writer固有の適用ルール
mappings/article-creator/  Article Creator固有の適用ルール
validation/                共通知識の品質検証基準
tests/                     リポジトリ整合性テスト
docs/                      運用・統合ドキュメント
```

## 利用原則

1. 共通知識の変更はこのリポジトリで行う。
2. WriterとArticle Creatorは、リリース済みバージョンから生成した「製品別スコープ済みスナップショット」を取り込む。
3. 製品側で共通知識を独自編集しない。
4. 製品への取り込み後は、各製品の回帰テストを実行する。

## Version

`3.2.0`


## v1.1.1 Operational Learning
中心主張、Evidence表現、データ不足時の縮退、購入情報鮮度を共通ルールとして追加しました。


## v1.1.3 Product-scoped snapshots

完全なShared Repositoryには両製品のmappingを保持しますが、各Claude Projectへ同梱するsnapshotには対象製品のmappingだけを含めます。詳細は `docs/product-scoped-snapshot-policy.md` を参照してください。


## v2.0.0 RC1 Four-Layer Architecture
Knowledge / Strategy / Evidence / Patternを分離し、修正前にEditorial Strategyを確定します。


## v2.1.0 Quality Pattern Library
運用試験で発見した再発防止ルールをRegistry化し、記事固有修正・Mapping不具合・Validation不具合を区別します。

## v2.3 Publication Integrity

Shared Editorial KnowledgeはSEO知識集に限定せず、SIMS製品共通の編集品質基準を提供します。v2.3では変動情報、マーケティング主張、アフィリエイトCTA、FAQ、本文とJSONの同期を正本化しました。


## v2.4 Real-article Validation

実記事Beforeの厳格照合、事実根拠境界、YMYL全体整合、8事例の回帰fixtureを追加しました。


## v3.0.1
SEO Critical Validation, internal auto-repair, revalidation, and publication finalization were added. Minor quality recommendations no longer block publication.

## v3.0.2

曖昧な料金・手数料表現を主体別に分解し、関連箇所を横断修正して再ValidationするHotfixです。


## v3.2.0 SBM-centered Platform Contracts

SBMをSIMS Editorial Platformの運営・記録・状態管理の正本として確定しました。CaseIDはSBMが発行し、Doctorは診断・Treatment Plan・ReferralをSBMへ返却します。Writerなどの専門製品への依頼と治療結果の受領もSBMを経由します。旧Doctor直結契約は互換用として残しますが、新規実装では使用しません。
