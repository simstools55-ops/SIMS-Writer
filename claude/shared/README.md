# SIMS Shared Editorial Knowledge

SIMS WriterとSIMS Article Creatorが共有する編集品質基準の正本（Single Source of Truth）です。

## 目的

- 両製品で共通するSEO・編集・Evidence知識を一元管理する
- 共通知識と製品固有の適用ルールを分離する
- WriterのPreservation思想とCreatorの新規設計思想を混同しない

## 構成

```text
knowledge/                 共通知識の正本
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

`1.0.0`


## v1.1.1 Operational Learning
中心主張、Evidence表現、データ不足時の縮退、購入情報鮮度を共通ルールとして追加しました。


## v1.1.3 Product-scoped snapshots

完全なShared Repositoryには両製品のmappingを保持しますが、各Claude Projectへ同梱するsnapshotには対象製品のmappingだけを含めます。詳細は `docs/product-scoped-snapshot-policy.md` を参照してください。
