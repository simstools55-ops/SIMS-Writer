# Operational Learning Promotion Policy

## Decision

運用試験で得た知見は、毎回Sharedへ無条件追加するのではなく、再利用性と既存ルールの有無を確認して昇格します。

## Classification

- **ARTICLE_SPECIFIC**: 固有名詞、現在値、URL、記事固有の不足。Sharedへ追加しない。
- **PATTERN_CANDIDATE**: 複数記事で再発し得る編集パターン。既存ルールを照合する。
- **MAPPING_DEFECT**: Sharedには存在するが製品で適用されていない。Mapping/Runtimeを修正する。
- **VALIDATION_DEFECT**: ルールは適用済みだが最終出力を通過した。Validationとテストを修正する。
- **PREFERENCE_ONLY**: 複数の自然な正解があり、品質違反ではない。新規ルール化しない。

## Promotion Threshold

次のいずれかを満たす場合に共通Patternへ昇格できます。

1. 異なる2記事以上で同種の問題が再発した
2. 1回でも安全性・事実性・契約整合へ重大な影響を与える
3. 既存品質ゲートの明確な盲点を示した

## Ownership

- Shared: product-neutral rule and canonical pattern
- Writer Mapping: existing-article editing application
- Creator Mapping: new-article planning application
- Product Runtime: execution order and contract-specific behavior
