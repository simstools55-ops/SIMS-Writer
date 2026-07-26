# RC2 Final Output Validator

## Contract Gate
- `contract_version`は`4.0`のみ。
- `publication_result`配下に2種類の変更配列を置く。
- Schemaで禁止された旧フィールドがあればFAIL。

## Evidence Gate
- 変動仕様のMULTIPLE_THIRD_PARTYはUSER_DECISION以下。
- 未確認事実がタイトル、メタ、導入、見出し、FAQ、本文のPUBLIC_OKへ一箇所でも混入したらFAIL。

## Visibility Gate
通常利用者向け本文に次があればFAIL：
- IMPROVEMENT_RECOMMENDED等の内部判定コード
- Validation/QA/SWLS/Coverage
- Evidence階層や内部Confidence
- 内部リンク不採用候補の一覧表

## Completeness Gate
- Before/Afterに「以下略」「原文全体」「改善後全文」等の省略表現を使わない。
- PUBLIC_OKはそのまま反映できる完成文にする。
