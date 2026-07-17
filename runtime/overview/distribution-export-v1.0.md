# Distribution Export v1.0

確定済みの公開スナップショットだけを外部配布用ZIPへ変換する。

## Safety Rules

1. `finalization-manifest.json` が finalized / release_ready であること。
2. release配下の全ファイルがFinalization時のSHA-256と一致すること。
3. ZIP作成後に破損検査、収録ファイル検査、個別SHA-256検査を行うこと。
4. 未確定または改変済みの成果物は拒否すること。

## Output

- `distribution/sims-writer-publication-<execution_id>.zip`
- `distribution/distribution-manifest.json`
