# Runtime Core v1.0

Runtime Coreは、正式資産を読み込み、Contractに従って11 Stageを制御する実行層です。

```text
Intake → Normalization → Source Acquisition → Knowledge Assembly
→ Content Planning → Decision Evaluation → Pattern Selection
→ Content Production → Quality Validation → Refinement
→ Publication Packaging
```

Alpha 1では、状態遷移、資産Version固定、入力Adapter、追跡可能な成果物の生成を実装します。記事本文の実生成はModel Adapterの責務として分離します。
