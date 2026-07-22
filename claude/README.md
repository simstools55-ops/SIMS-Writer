# SIMS Writer RC3 Claude Package

このフォルダーは、SIMS Writer v0.15.3-alpha.1をClaude Projectへ登録するためのファイル一式です。

## Claudeへ登録するファイル

1. `CLAUDE_PROJECT_INSTRUCTIONS.md`
   - Claude Projectの「Project Instructions」へ全文を貼り付けます。
2. `knowledge/SIMS_WRITER_KNOWLEDGE_PACK.md`
   - Claude Projectの「Project Knowledge」へアップロードします。

既存のSIMS Writer用InstructionsとKnowledgeは削除または差し替え、旧版と混在させないでください。

## テスト

更新後は、まずA000008相当の依頼を`partial`モードで実行し、次を確認します。

- 全文が出ない
- Before / After / 理由が出る
- JSONが最後に1つだけ出る
- JSON後に文章がない
- `main_query`へ説明文が混ざらない
- 本文セクション追加時は`changes.body=true`
- 未確認URLが`adopted`にならない


## v1.1.2 Sprint 1 product guides

Claude Projectは`product/quality/QUALITY_FRAMEWORK.md`、`product/platform/SIMS_PLATFORM_GUIDE.md`、`product/roadmap/WRITER_v1.1.2_IMPROVEMENT_PLAN.md`をWriter本体と同一内容で参照します。
