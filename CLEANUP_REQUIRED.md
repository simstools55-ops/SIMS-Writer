# Cleanup required for v3.3.0

GitHubへ上書きした後、旧Repositoryに残っている次の項目を削除してください。

- `src/doctor/`
- `claude/`（Writer Claudeは別Repositoryで管理）
- `contracts/SIMS_DOCTOR_*.schema.json`
- `contracts/schemas/SIMS_DOCTOR_*.schema.json`
- Doctor専用の旧Runtime／Testファイル

今回のZIPには削除済み状態が収録されていますが、単純上書きではGitHub上の旧ファイルは消えません。
