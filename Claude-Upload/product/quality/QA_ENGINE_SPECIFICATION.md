# SIMS Writer QA Engine Specification v1.0

## 1. 目的

Writerが生成した改善案を公開前に独立評価し、安全に修正できる問題はその場で修正したうえで、公開可能な最終版だけを提示する。

## 2. 配置

QA Engineは新しい製品を増やすのではなく、Writer RuntimeのStage 9〜11を統括するサブシステムとする。

```text
Content Production
  -> Publication QA（初回評価）
  -> Targeted Refinement（安全な限定修正）
  -> Publication QA（再評価）
  -> Publication Packaging
```

## 3. 判定

- `PASS`: そのまま公開可能
- `PASS_WITH_WARNING`: 公開可能。注意事項を残す
- `PASS_WITH_MINOR_FIX`: 安全な軽微修正を適用済み。修正版を公開可能
- `PASS_WITH_REQUIRED_FIX`: 公開停止。修正後の再評価が必要
- `FAIL`: 公開停止。人による判断または改善案の再生成が必要

## 4. 評価領域

1. 記事公開品質
2. SEO判断
3. Winner Query Preservation
4. 編集・保全品質
5. 数値・論理・事実整合性
6. 内部リンク品質
7. SIMS_FEEDBACK Contract
8. Validation自己整合性
9. 回帰品質
10. YMYL・安全性

## 5. 非破壊原則

QAは第二のWriterにならない。明確な局所欠陥だけを修正し、主要結論、検索意図、体験談、独自評価、Winner Queryを独断で変更しない。

## 6. 出力

公開パッケージには次を含める。

- 初回判定
- 最終判定
- 自動修正の有無
- 修正記録
- 残存リスク
- 公開アクション
- 最終版のタイトル、メタ、本文、JSON
