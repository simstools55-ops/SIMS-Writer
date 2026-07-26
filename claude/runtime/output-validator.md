# RC Final Output Validator

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
- 内部リンク不採用候補の一覧表、候補件数、補足説明

## UX Gate
- 回答冒頭に公開可否を示す一文がない場合はFAIL。
- 利用者判断がなければ「今回の修正は、そのまま公開できます。」相当を表示する。
- 利用者判断があれば「公開OKは反映可能で、判断項目だけ確認」と明示する。
- 公開OKの理由が2文以上、またはSEO用語・文字数基準・SERP・Evidenceを含む場合はFAIL。
- 内部リンク全件不採用時は「今回は追加できる内部リンクはありません。」の一文以外を表示したらFAIL。

## Completeness Gate
- Before/Afterに「以下略」「原文全体」「改善後全文」等の省略表現を使わない。
- PUBLIC_OKはそのまま反映できる完成文にする。


## SERP Gap Report Gate
- SERPが修正判断に使われた場合、短い比較結果を公開OKの前に置く。
- 強み・不足・適用・非適用を、利用者向け平易表現で示す。
- 競合にあるだけの項目をGap扱いしない。
- 未確認の件数・掲載率・上位10件比較を捏造しない。
- Contract 4.1の`publication_result.serp_gap_report`と表示内容を一致させる。
