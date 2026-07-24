# SIMS-Core Migration Framework v1.0

## 目的

SIMS-Coreの有効な知見をSIMS Writerへ継承しつつ、Engine中心設計、Prompt依存、重複命令を新製品へ持ち込まないための正式な移行手順を定義する。

## 原則

1. 旧ファイル単位ではなく、判断・知識・失敗・成果物の単位で評価する。
2. Raw資産は `archive/sims-core/raw/` に不変保存する。
3. 評価結果は Keep / Adapt / Archive / Remove の4分類とする。
4. KeepまたはAdaptでも、Knowledge・Decision・Pattern・Quality Rule・Golden Caseへ変換後にのみactive化できる。
5. 出典、適用範囲、Version、検証結果がない資産をRuntimeへ接続しない。
6. Prompt表現そのものをProduct Coreへ移植しない。

## 移行フロー

```text
Raw Asset
→ Inventory
→ Statement / Decision / Pattern Extraction
→ Evidence Review
→ Keep / Adapt / Archive / Remove
→ Target Asset Conversion
→ Contract Validation
→ Golden Test
→ Review
→ Active Registration
```

## 分類基準

### Keep

内容、根拠、責務がSIMS WriterのCore Principlesに適合し、最小限の形式変換だけで利用できる。

### Adapt

知見は有効だが、EngineやPromptに埋め込まれている、責務が混在する、適用条件が不足するなどの理由で再設計が必要。

### Archive

歴史的価値や比較価値はあるが、現行Runtimeで利用しない。

### Remove

誤り、重複、過剰複雑、モデル依存、理由のない固定処理、品質低下などのため継承しない。

## active化条件

- 元資産と移行先を追跡できる
- 根拠または運用実績がある
- 適用・非適用条件が明確
- 既存資産と重複しない
- Contractに適合する
- Golden CaseまたはReview Evidenceがある
- 特定モデルのPrompt表現に依存しない
