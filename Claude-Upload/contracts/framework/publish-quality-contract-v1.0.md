# Publish Quality Contract v1.0

## Purpose

Product 1.0の主力であるpartialモードに、編集者としての変更判断と説明責任を追加する。

## Required Assessment

- `improvement_judgment`: `improvement_recommended` / `minor_improvement` / `maintain_current`
- `search_intent`: `comparison` / `purchase` / `informational` / `troubleshooting` / `how_to` / `unknown`
- `estimated_minutes`: 反映作業の目安。現状維持は0分を許可する

## Difference Format

変更項目は次の順序で出す。

1. Before
2. After
3. 期待する効果
4. 理由

変更しない主要項目を説明する場合は、`変更なし`と`変更しない理由`を示す。

## Comparison Article Gate

比較意図の記事では次を確認する。

- 比較項目が明示されている
- 比較要約と最終結論が一致する
- それぞれをおすすめする人が示されている
- 推奨商品が比較結果と矛盾しない

## Forecast Guard

期待する効果に、根拠のないCTR、クリック数、順位の数値予測を含めない。
