# Orchestrator Specification

OrchestratorはStage順序、状態、再試行、停止、再開地点を管理します。正式KnowledgeやQuality判断の内容は保持しません。

- Blocked Stageの後続は実行しない
- Execution中の資産Versionは固定する
- 同一Requestの再実行は新しいexecution_idを付与する
- Errorは共通Error Contractへ変換する
