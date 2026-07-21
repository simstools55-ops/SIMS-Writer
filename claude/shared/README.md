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
2. WriterとArticle Creatorは、リリース済みバージョンの検証済みスナップショットを取り込む。
3. 製品側で共通知識を独自編集しない。
4. 製品への取り込み後は、各製品の回帰テストを実行する。

## Version

`1.0.0`
