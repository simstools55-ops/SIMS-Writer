# Publication Package Contract

- Contract ID: `CT-PUB-001`
- Version: `1.0.0`
- Status: `draft`

## 目的

Publication Package の入力・出力構造を定義し、曖昧な受け渡しを防ぎます。

## 検証

1. JSON Schema Draft 2020-12による形式検証
2. 項目間整合性を確認するSemantic Validation
3. Product要件を確認するBusiness Validation

## ファイル

- `publication-package.schema.json`
- `examples/valid.json`
- `examples/invalid.json`

## 互換性

Semantic Versioningを使用します。未知のMajor Versionは自動処理しません。
