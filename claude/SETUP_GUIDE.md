# Claude Project Setup Guide

Version: 1.6.0-preview.1
Status: Developer Preview

> このパッケージは構成検証用です。一般利用者テストはまだ開始しません。

## Claudeへ登録するファイル

### Project Instructions

`CLAUDE_PROJECT_INSTRUCTIONS.md`の全文をClaude ProjectのProject Instructionsへ設定します。

### Project Knowledge

次の1ファイルをProject Knowledgeへ追加します。

- `knowledge/SIMS_WRITER_KNOWLEDGE_PACK.md`

### 入力テンプレート

改善依頼を作る際は、次のファイルを複製して使用します。

- `templates/IMPROVEMENT_REQUEST_TEMPLATE.json`

## 開発者確認手順

1. Project Instructionsを設定する。
2. Knowledge Packを追加する。
3. `examples/EXAMPLE_REQUEST.json`の内容をClaudeへ送る。
4. JSON以外の前置きが出ないことを確認する。
5. 必須キーと`status`を確認する。
6. 本文を削除して再実行し、`manual_review_required`になることを確認する。

## 利用者テスト開始条件

- Claude出力Schemaの自動検証が合格する
- Golden UATがClaude Project上で合格する
- 日本語記事品質の実記事UATが合格する
- セットアップ手順が初心者環境で再現できる
- 配布ZIPの内容と登録対象が確定する
