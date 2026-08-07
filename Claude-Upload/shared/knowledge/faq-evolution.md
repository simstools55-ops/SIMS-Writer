# FAQ Evolution

## Purpose

FAQは件数を増やすためではなく、本文を読んだ後にも残る、判断・行動に影響する疑問を解消するために進化させる。

## Detection

FAQ候補は次のすべてを満たす場合だけ採用する。

1. メインクエリ、Supporting Query、Hidden Anxiety、本文内の例外・制約のいずれかに根拠がある。
2. 本文ですでに十分回答されていない。
3. 回答により読者の判断、実行、失敗回避のいずれかが改善する。
4. 本文の見出しを言い換えただけではない。

## Evolution actions

- `add`: 根拠付きの残存疑問があり、既存FAQに回答がない。
- `revise`: 既存FAQは関連するが、質問または回答が曖昧・古い・不十分。
- `merge`: 複数FAQが同じ疑問を重複している。
- `remove`: 本文と完全重複、検索意図から外れる、または根拠がない。
- `keep`: 判断支援として有効で、本文と役割分担できている。

## Guardrails

- FAQ数の目標値を設けない。
- Supporting Queryを機械的に質問化しない。
- 根拠のない不安を新たに作らない。
- Change BudgetとRewrite Level/Scopeを上書きしない。
- JSON Contractの変更を要求しない。
