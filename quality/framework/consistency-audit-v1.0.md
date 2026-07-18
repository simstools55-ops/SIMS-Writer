# Consistency Audit v1.0

## Numeric consistency
時間、件数、価格、割合、順位、日数、年齢、商品数、FAQ数をタイトル・導入・本文・FAQ・まとめ間で照合する。

## Scope consistency
「完全」「すべて」「全機種」「年代別」「種類別」「コピペOK」など、対象範囲を拡張する表現が本文で満たされるか確認する。

## Output consistency
改善必要度、変更箇所、Before/After、確認事項、JSONの変更フラグ・新値・次アクションを照合する。

## Required result
重大な不一致は `fail` とし、最終出力前に修正する。
