# SIMS Writer v1.1.0-rc2 Release Notes

## Purpose

独立リポジトリ`SIMS-Shared-Editorial-Knowledge v1.0.0`を共通知識の正本とし、Writerへ検証済みスナップショットとして取り込む依存管理方式を確立する。

## Changes

- `shared/`を正本のディレクトリ構成に合わせて再編。
- `VERSION`、`SOURCE.md`、`SNAPSHOT_MANIFEST.json`を追加。
- Writer側での直接編集を禁止し、正本更新→バージョン更新→製品統合テストの手順を明文化。
- Claude配布版にも同一スナップショットを同梱。
- スナップショットの必須資産とSHA-256を検証する回帰テストを追加。

## Shared dependency

- Repository: `SIMS-Shared-Editorial-Knowledge`
- Version: `1.0.0`
- Integration mode: vendored read-only snapshot

## Compatibility

v1.1.0-rc1で追加したProduct 5.3.1識別情報透過対応、SEO品質改善、Validation、後方互換性を維持する。
