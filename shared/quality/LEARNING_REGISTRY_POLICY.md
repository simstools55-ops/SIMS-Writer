# Learning Registry Policy v1.0

## Purpose

実記事試験のフィードバックを、即時の個別修正と製品共通の学習に分離し、同じ議論とリリースの繰り返しを防ぎます。

## Mandatory order

`Observe → Classify → Existing-rule check → Decide → Implement if required → Regress → Close`

修正案を先に作り、後から分類してはいけません。

## Classification authority

- ARTICLE_SPECIFIC: 記事へ反映可能。Shared更新なし。
- PATTERN_CANDIDATE: Quality Pattern Libraryへの昇格審査。
- MAPPING_DEFECT: Shared正本は変えず、配布経路を修正。
- VALIDATION_DEFECT: 既存ルールを最終QAへ接続し回帰テストを追加。
- PREFERENCE_ONLY: 製品変更なし。

## State transition

`NEW → TRIAGED → ACCEPTED/REJECTED/DUPLICATE → IMPLEMENTED → VERIFIED → CLOSED`

ARTICLE_SPECIFICとPREFERENCE_ONLYは、決定理由を記録したうえで直接CLOSEDにできます。

## Promotion boundary

Quality Patternへ昇格するには、次のいずれかが必要です。

- 異なる2記事以上で再発
- 1件でも安全性、事実性、Contractへ重大な影響
- 既存ゲートの明確な盲点

## No-release-noise rule

記事固有の修正、表現上の好み、既存ルールで正常に処理できたケースだけでは新バージョンを作りません。
