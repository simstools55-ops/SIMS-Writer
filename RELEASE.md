# SIMS Writer Repository v0.4.0

## Release Scope

改善依頼、記事本文、検索指標を使い、外部LLMなしでも保守的なCTR改善案を生成する最初の実用Vertical Slice。

## Implemented

- 決定的CTR改善AdapterをRuntime既定Adapterとして接続
- SEOタイトル、導入文、FAQの改善提案生成
- 現行値と改善後を比較するBefore / After生成
- 改善理由の構造化出力
- Search Console指標と補助クエリに基づく判断
- Knowledge選択とContent PlanのRuntime実接続
- 本文未提供時のmanual_review_required維持
- End-to-End Runtime統合テスト

## Release Gate

```bash
python tools/test_repository.py
```

全項目合格したRepositoryのみ配布対象とする。
