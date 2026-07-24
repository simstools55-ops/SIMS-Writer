# SIMS Writer v1.1.2 Improvement Plan

Version: 1.2.0  
Status: Approved Implementation Plan  
Release method: Sprint

## 1. 目的

v1.1.2は、合意済み設計を実装資産へ固定し、SIMS Writer、Shared Editorial Knowledge、Claude Projectの責務と品質運用を明文化する改善リリースである。

本計画は設計の再検討を行わない。既存のProduct Philosophy、Contracts、Knowledge、Patterns、Quality Rules、Runtime、Shared Repository連携を変更せず、実装と同期を段階的に完了させる。

## 2. リリース原則

- Sprintごとに対象を限定する。
- 各SprintはGitHubへそのまま反映できる完全資産で完了させる。
- Shared Repositoryを製品横断Knowledgeの唯一の正本として維持する。
- Writer固有の品質・表示・プラットフォーム規則をSharedへ移管しない。
- Writer本体とClaude Projectの同期をリリースゲートとする。
- Preservation、Change Budget、Rewrite Level/Scope、Canonical JSON、後方互換を維持する。
- 設計追加は行わず、既存設計の実装不足だけを解消する。

## 3. Sprint構成

### Sprint 1: Platform・Quality・Roadmap文書

作成対象:

1. `product/platform/SIMS_PLATFORM_GUIDE.md`
2. `product/quality/QUALITY_FRAMEWORK.md`
3. `product/roadmap/WRITER_v1.1.2_IMPROVEMENT_PLAN.md`

反映対象:

- SIMS Writer本体
- Shared Editorial KnowledgeのWriter application mapping
- Claude Project配布物
- VERSION / CHANGELOG / README / Release Notes
- manifest / checksum
- Sprint 1回帰テスト

完了条件:

- 3文書が既存実装を正しく参照し、新しい仕様を作っていない。
- SharedとWriterの責務境界が明確である。
- Claude Projectに3文書が同梱され、参照順が明記される。
- version、manifest、checksum、テストが整合する。

### Sprint 2以降

Sprint 2以降は、設計フェーズで承認済みの実装順に従う。対象は各Sprint開始時に確定済み項目だけを実装し、この文書から新規要件を派生させない。

Sprint 1完了時点では、次Sprintの機能追加、Knowledge追加、Contract変更、Runtime変更を先行実装しない。

## 4. Repository別の実装責務

### 4.1 SIMS Writer

- Product Guideの正本を保持する。
- Quality Frameworkと既存Quality資産を接続する。
- Platform GuideとSite Fit Ruleを接続する。
- Claude Project用資産を本体内`claude/`へ同期する。
- 回帰テスト、manifest、release metadataを管理する。

### 4.2 Shared Editorial Knowledge

- 製品横断Knowledgeの内容は変更しない。
- Writer application mappingへ、Platform GuideとQuality Frameworkの適用境界を記録する。
- Writer固有のQuality Gate、出力形式、CMS構文をShared Knowledgeとして登録しない。

### 4.3 Claude Project

- Writerで確定した3文書を同梱する。
- Project Instructionsから参照順を示す。
- 独自解釈や別版の品質基準を持たない。
- Shared snapshotを読み取り専用で利用する。

## 5. 互換性要件

v1.1.2 Sprint 1では次を変更しない。

- SIMS Feedback JSONの必須構造
- Product 5.3.1識別情報の受け継ぎ
- 旧URL入力の後方互換
- Improvement Type
- Confidence
- Execution Mode
- Preservation Score
- Change Budget
- Rewrite Level / Scope
- Diagnosis / Warning / Information
- Internal Linkの採用・保留・不採用
- Shared snapshotの実行時外部取得禁止

## 6. 品質保証

Sprint 1で追加するテストは文書実装と同期だけを検証する。

- 必須3文書の存在
- version表記
- 必須見出し
- Writer本体とClaude Projectの内容一致
- Shared mappingの責務境界
- manifest/checksumの整合
- 既存全回帰テストの継続合格

文書追加によってRuntime判断結果が変化してはならない。

## 7. リリース成果物

- `SIMS-Writer-v1.1.2-Sprint1.zip`
- `SIMS-Writer-Claude-v1.1.2-Sprint1.zip`
- `SIMS-Shared-Editorial-Knowledge-v1.1.2-Sprint1.zip`

各ZIPはリポジトリルートを一つ含み、GitHub上の対応リポジトリへ上書き反映できる構成とする。

## 8. Sprint 1受入基準

- [x] 設計変更を行っていない。
- [x] 指定された3文書を実装した。
- [x] Shared Repositoryへ必要最小限のmapping反映を行った。
- [x] Writer本体とClaude Projectへ同一文書を反映した。
- [x] release metadataをv1.1.2へ更新した。
- [x] 回帰テストを追加した。
- [ ] 全テスト合格を確認する。
- [ ] ZIP内容とSHA-256を確認する。

最後の2項目は成果物生成時の検証結果をもって完了とする。
