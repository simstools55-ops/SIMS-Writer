# Quality Foundation Contract v1.0

Release: v0.16.0-alpha.1

## Purpose
実記事テスト10件で確認された、検索診断・整合性・出力Contractの再発問題を出力前に検証する。

## Improvement type
- `minor`: 限定的な変更で改善可能。本文構造に大きな問題がない。
- `normal`: 複数箇所の改善または本文の部分修正が必要。
- `major`: 全面改稿、検索意図再設計、統合または重大な信頼性修正が必要。

日本語表記は `軽微改善 / 改善推奨 / 大幅改善` と対応させる。

## Confidence
- `high`: 必須入力が揃い、重大warning・推定・未解決矛盾がない。
- `medium`: warning、未確認事項、保留判断、更新性の高い情報のいずれかがある。
- `low`: 主要入力欠損、重大矛盾未解決、改善案を確定できない。

重大warningがある状態で `high` を使用しない。

## Execution mode
- `standard`: 記事ID、URL、タイトル、メインクエリ、Search Console概要、本文、改善目的が利用可能。
- `graceful_degradation`: 主要入力の一部を推定または限定判断で補う。

`graceful_degradation` の場合、`estimated_fields` は1件以上必要。

## Next action
- SEOタイトルまたはメタディスクリプションを変更した場合は原則 `remeasure`。
- 変更なしは `monitor`。
- 大規模再構成は `rewrite`。
- 追跡不要は `none`。

## Change flags
`changes` は実際にAfterへ反映した変更だけを `true` とする。評価・保留のみでは変更扱いにしない。
