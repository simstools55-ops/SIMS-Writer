# SIMS Writer v1.3.2 Publication QA Foundation

## Summary

Writerの改善案を公開前に独立評価し、安全な軽微修正、再評価、公開判定を統括するPublication QA Engineの基礎を追加しました。

## Added

- PublicationQAEngine
- 5段階QA判定
- Safe Auto-Fix境界
- Publication Release Gate
- ADR-0020
- Official Regression Suite v1の受け皿と5ケース台帳
- Claude Project用Publication QA必須工程
- Shared Knowledgeの共通QA原則

## Compatibility

既存のRuntime `status` と `publish_recommendation` は維持します。新しいQA判定は `artifacts.publication_qa.final_verdict` と publication packageの `qa_verdict` に追加されます。

## Validation

Writer: 92 passed, 3 skipped.
Shared Knowledge: 12 passed.
