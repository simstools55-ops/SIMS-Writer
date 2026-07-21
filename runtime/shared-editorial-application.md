# Shared Editorial Knowledge Application v1.1.0

## Purpose

SIMS-Shared-Editorial-Knowledge v1.0.0をWriterのPreservation制約下で実行可能な診断信号へ変換する。

## Processing order

1. Intent GapをLOW / MEDIUM / HIGHで評価する。
2. Supporting Queryまたは対象特性に根拠があり、本文で未回答のHidden Anxietyだけを抽出する。
3. タイトル・主クエリからSERP Entityを保護対象として記録する。
4. Evidenceを公式・独立第三者・UGC・検索スニペット・未確認へ分類する。
5. 内部リンク候補を意味的補完性、自己リンク、URL確認状況で採否判定する。
6. Decision Supportは既存記事に同等機能がない場合だけ提案する。

## Guardrails

- 各信号はPreservation Score、Change Budget、Rewrite Level、Rewrite Scopeを上書きしない。
- HIGH Intent Gapだけを理由に全面リライトしない。
- Hidden Anxietyを網羅目的で追加しない。
- SERP Entityの削除は、検索文脈をより正確にする明示的理由がある場合だけ許可する。
- Evidenceの強さを超える断定をしない。
- 文字列一致だけの内部リンクは採用しない。

## Runtime artifact

`artifacts.editorial_signals`へ次を保存する。

- `intent_gap`
- `hidden_anxiety`
- `serp_entity_preservation`
- `internal_link_semantics`
- `evidence_transparency`
- `decision_support_policy`
- `preservation_guard`
