# Gate Rules v1.0

## 優先順位
`BLOCKING > STRUCTURAL_CONFLICT > REVIEW > WARNING > PASS`

## Blocking
Blocking Rule Registryに1件以上一致した場合、`BLOCK`かつ`output_allowed=false`。

## Strategy矛盾
- Preservation 90以上 + L4/L5
- LOW_SAMPLE + L4/L5
- PROTECT_WINNER + タイトル全面変更
- Change Budget 15% + planned 60%
- L1 + S5
- L5 + S1
- no_change + changesあり
- full_rewrite_candidate + protected_elementsなし
- HIGH Risk + rationaleなし

重大な矛盾は`REVIEW_REQUIRED`。

## Review条件
- Confidence LOWかつRisk HIGH
- Preservation 75以上でL4以上
- Budgetを20ポイント以上超過
- 高CTRタイトル変更
- 改善後28日未満で構造変更
- 監査結果が複数矛盾

## Warning
Warningがあり、Blocking/Reviewがなければ`PASS_WITH_WARNING`。

## Rule Trace
すべての判定で発火・非発火ルールを保持する。
