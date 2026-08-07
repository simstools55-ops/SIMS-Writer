# Publication Release Gate v1.0

| 最終判定 | 公開 | 処置 |
|---|---:|---|
| PASS | 可 | 最終版を出力 |
| PASS_WITH_WARNING | 可 | 注意事項付きで最終版を出力 |
| PASS_WITH_MINOR_FIX | 可 | 自動修正版を最終版として出力 |
| PASS_WITH_REQUIRED_FIX | 不可 | 対象箇所を修正し再評価 |
| FAIL | 不可 | 人による確認または改善案再生成 |

## 必須停止条件

- 記事内の明白な数値矛盾
- 本文とFAQの主要事実矛盾
- YMYLの危険な断定
- 体験・専門性の捏造
- 必須Contract欠落によりSBM登録不能
- 未確認内部リンクを実装済みと表示
- Winner Queryを根拠なく破壊
- Validationが既知の重大不整合をPASSとしている
