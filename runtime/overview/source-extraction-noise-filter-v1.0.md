# Source Extraction Noise Filter v1.0

SIMS Writerは、取得したHTMLから記事本文を抽出する際、記事外の共通UIを決定的に除去します。

## 除去対象

- header / nav / footer / aside / form
- 広告、関連記事、ランキング、共有ボタン、サイドバー、購読UI
- script / style / iframe / template等の非本文要素
- `aria-hidden=true`または`hidden`要素

## 安全方針

除去判定はタグ、role、id、classに限定します。本文中の「おすすめ」「関連記事」などの語だけでは除去しません。

## 追跡情報

Source Snapshotへ以下を記録します。

- `extraction_profile`: `article-aware-noise-filter-v1`
- `removed_noise_count`: 除去した要素数
