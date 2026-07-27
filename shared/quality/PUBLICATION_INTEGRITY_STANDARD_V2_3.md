# Publication Integrity Standard v2.3

## Mandatory gates

PUBLIC_OKへ入れる変更は、次をすべて満たす。

1. Official/Freshness Gate
2. Marketing Claim Gate
3. Affiliate CTA Gate
4. FAQ Consistency Gate
5. Cross-component Consistency Gate
6. Publication/JSON Synchronization Gate

## Failure routing

- 現在有効な一次情報で確認済み: PUBLIC_OK候補
- 変動情報を第三者情報だけで確認: USER_DECISION以下
- 推測、未確認、不一致、古い可能性: INTERNAL_REJECTまたは修正

## Marketing claims

「最安値」は比較対象と確認時点を明示できる場合だけ使用する。公式価格を確認しただけでは市場最安値を意味しない。

## Correction requests

指定箇所の局所修正では、対象外を再設計しない。修正文、reason、change_summary、JSON全体を同期して再出力する。
