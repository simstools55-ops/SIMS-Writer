# Learning Sprint Playbook

## Cadence

実記事10件を1バッチとして集計します。重大な安全性・契約不具合は10件を待たず即時処理します。

## Per-article flow

1. SBM依頼をWriterへ投入する
2. 記事へ反映する前にWriter回答を保存する
3. 回答を5分類のいずれかへトリアージする
4. 公開OK部分は、分類結果と安全性を確認後に記事へ反映する
5. `PATTERN_CANDIDATE`は既存Quality Patternとの重複を確認する
6. `MAPPING_DEFECT`はSnapshot/Runtime接続を修正する
7. `VALIDATION_DEFECT`は最終ゲートと回帰テストを修正する
8. `PREFERENCE_ONLY`では製品を変更しない

## Ten-article review

次を集計します。

- 分類別件数
- 同一Pattern IDの再発数
- 未処理Learning
- Mapping/Validation defectの再発
- Sharedへ昇格したルール
- 却下・Preference判定

## Release rule

各記事の細かな表現差ではリリースしません。次の場合だけ製品版を更新します。

- 新しい共通Patternを採用した
- Mapping defectを修正した
- Validation defectを修正した
- 安全性・契約互換に重大な修正が必要

通常のARTICLE_SPECIFICとPREFERENCE_ONLYは次回リリースへ持ち込みません。
