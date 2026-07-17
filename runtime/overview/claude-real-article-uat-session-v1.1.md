# Claude Real Article UAT Session v1.1

実記事UATの入力、Claude応答、検証結果、採点証拠を同一Session IDで追跡するための運用仕様です。

## 原則

- UAT開始時点では結果や点数を作成しない。
- 依頼JSONのSHA-256を証拠テンプレートへ固定する。
- 同一セッション内の記事ID重複を拒否する。
- Claude応答とRuntime検証結果は別ファイルとして保存する。
- 実測後だけ`pending`を正式な結果へ変更する。
