# SIMS Writer Repository v0.6.0

## Release Scope

Runtimeが生成した公開成果物を、配布前に決定論的に検証し、改ざん・欠落・不整合を発見できるVertical Slice。

## Implemented

- 必須成果物5点の存在・空ファイル検査
- UTF-8 JSONとしての読込検査
- Execution ID / Request IDの成果物間整合性検査
- Publication Package必須項目検査
- 記事MarkdownのH1・本文検査
- 各成果物のSHA-256とバイト数記録
- Artifact StatusとRelease Readyの明示判定
- `artifact-validation.json`生成
- `publication-checklist.md`生成
- 欠落・ID不一致を公開停止する回帰テスト

## Generated Files

- `runtime-result.json`
- `publication-package.json`
- `article.md`
- `improvement-report.md`
- `execution-manifest.json`
- `artifact-validation.json`
- `publication-checklist.md`

## Release Gate

```bash
python tools/test_repository.py
```

全項目合格し、ZIP再展開後も同一Release Gateに合格したRepositoryのみ配布対象とする。
