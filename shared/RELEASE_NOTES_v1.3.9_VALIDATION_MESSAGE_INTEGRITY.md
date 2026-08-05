# v1.3.9 Validation Message Integrity Hotfix

- Validationの空メッセージ正例をWriter・Claude・Sharedから除去。
- `validation.checks[].message`を全ステータスで必須化。
- JSON Schemaへ`minLength: 1`と非空白パターンを追加。
- ルール別の具体的な自動補完辞書を追加。
- 汎用プレースホルダーを再補完対象化。
- `VAL-CONTRACT-006`を追加し、空・欠落・空白メッセージを最終出力停止条件化。
- リポジトリ全文走査テストとSchema拒否テストを追加。
