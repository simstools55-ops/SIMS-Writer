# Source Content Contract

- Contract ID: `CT-SRC-001`
- Version: `1.0.0`
- Status: `implemented-profile`

## 目的

既存記事改善で使用する本文入力と、Runtimeが生成するSource Snapshotを定義する。

## v0.3.0 Runtime入力

- `existing_content`: HTML、Markdown、プレーンテキストの記事本文
- `content_format`: `auto`、`html`、`markdown`、`plain_text`
- `target_url`: 出典URL。v0.3.0 Runtimeは外部ネットワーク取得を行わない

## Runtime Source Snapshot

- `status`: `available`、`missing`、`not_applicable`
- `source_type`: 現在は`request_payload`
- `content_format`: 検出または指定された形式
- `title`: 抽出タイトルまたは入力タイトル
- `headings`: 見出しレベルと本文
- `plain_text`: 品質判定・改善計画で利用する正規化本文
- `original_content`: 公開形式を保持した原文
- `character_count` / `line_count`: 入力充足度の補助指標
- `content_hash`: `sha256:`接頭辞付きの同一性確認値
- `warnings`: 短すぎる本文や見出し不足などの明示的警告

既存記事のURLだけがあり本文がない場合、Runtimeは推測で改善せず、`manual_review_required` とする。

## 互換性

既存のSource Content JSON Schemaは将来の直接取得・構造化抽出用の完全契約として維持する。v0.3.0のSource Snapshotは、その前段で使用するRuntime実装プロファイルである。
