# SIMS Writer Repository v0.2.0

## Release Scope

Improvement Request IntakeとArticle ContextをRuntimeへ接続した最初の入力Vertical Slice。

## Implemented

- SBM / Generic JSON自動判定
- JSON Schema検証
- 実データ向け安全な正規化
- Article Context生成
- Runtime Artifact接続
- CLI `auto` input type

## Release Gate

```bash
python tools/test_repository.py
```

全項目合格したRepositoryのみ配布対象とする。
