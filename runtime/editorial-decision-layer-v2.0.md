# Editorial Decision Layer v2.0

各修正候補を内部QA後に `PUBLIC_OK`、`USER_DECISION`、`INTERNAL_REJECT` のいずれかへ分類する。判定は記事単位ではなく修正単位で行う。

- `PUBLIC_OK`: 完成原稿であり、そのまま反映可能。
- `USER_DECISION`: 事実・体験・運営方針など利用者だけが確定できる。
- `INTERNAL_REJECT`: 根拠不足、未解決修正、Before/After不整合、非完成原稿。利用者へ表示しない。
