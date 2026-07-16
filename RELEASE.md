# SIMS Writer Repository v0.3.0

## Release Scope

既存記事本文をRuntimeへ安全に取り込み、改善判断の根拠となるSource Snapshotを生成するSource Acquisition Vertical Slice。

## Implemented

- HTML / Markdown / Plain Text自動判定
- タイトル・H1〜H6・本文抽出
- script / style等の非本文除外
- 原文保持と正規化本文生成
- 文字数・行数・SHA-256記録
- 短文・見出し不足の警告
- 本文未提供時の手動確認判定
- Runtime Source Acquisition Stage接続

## Release Gate

```bash
python tools/test_repository.py
```

全項目合格したRepositoryのみ配布対象とする。
