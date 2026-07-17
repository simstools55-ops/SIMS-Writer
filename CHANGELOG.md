# CHANGELOG

## 1.1.0

- 改善依頼JSONフォルダのバッチ処理を実装
- 記事ごとの独立成果物フォルダと安全なRequest ID整形を実装
- 1件失敗時も残りを継続するエラー分離を実装
- `batch-summary.json`と`batch-summary.md`を追加
- CLI `--batch-input`を追加
- 複数記事、要確認、壊れたJSON、重複Request IDのテストを追加

## 1.0.0

- 確定済み公開スナップショットの配布ZIP生成を実装
- 公開成果物とFinalization Manifestのチェックサム再検証を実装
- 配布ZIP内部の破損・内容・チェックサム検査を実装
- Distribution ManifestとZIP全体SHA-256を生成
- CLI `--export` を追加
- 未確定・改変済み成果物の配布拒否テストを追加

# Changelog

## 0.9.0

- Added pending review, approval, rejection, and finalization workflow.
- Added execution-bound approval records and append-only approval history.
- Added immutable release snapshots with SHA-256 finalization manifests.
- Added CLI approval operations and invalid-transition regression tests.

## 0.8.0

- Added safe artifact rollback from archived executions.
- Added rollback manifest, revalidation, CLI support, and tests.

## [0.7.0] - 2026-07-17

### Added
- Previous execution artifact archiving under `.history/<execution_id>/`
- `execution-history.json` for traceable rerun history
- `artifact-diff.json` for checksum and Publication Package comparison
- Rerun and history integration tests

### Changed
- Result Artifact output expanded from 7 to 9 top-level files

## 0.6.0 - Publication Artifact Validation

- Added deterministic validation for the persisted publication artifact set.
- Added UTF-8 JSON, required file, identifier consistency, package completeness, and Markdown checks.
- Added SHA-256 checksums and explicit artifact validity / release readiness results.
- Added `artifact-validation.json` and `publication-checklist.md` outputs.
- Added valid and invalid artifact-set regression tests.

## 0.5.0 - Structured Result Artifact Export

- Added a reusable artifact writer for every Runtime execution.
- Added complete article Markdown, improvement report, publication package, and execution manifest outputs.
- Updated the CLI to generate five reviewable files in one command.
- Added UTF-8, overwrite-safety, and artifact completeness tests.

## 0.4.0 - Deterministic Improvement Generation

- Added the deterministic CTR improvement adapter as the default runtime production adapter.
- Connected request metrics, source snapshot, knowledge selection, and content planning to proposal generation.
- Added SEO title, introduction, FAQ, before/after, and change-reason artifacts.
- Added end-to-end runtime tests for generated and missing-source paths.

## [0.3.0] - 2026-07-17

### Added
- HTML / Markdown / Plain Textの記事本文抽出器
- Source Snapshot（タイトル、見出し、正規化本文、文字数、SHA-256）
- Source Content ContractのRuntime実装プロファイル
- Source Acquisition Runtime統合テスト4件

### Changed
- Improvement Requestに`content_format`を追加
- URLのみで本文がない既存記事は`manual_review_required`として明示
- pytestをRepositoryルートから直接実行可能に修正

### Validation
- Repository Release Gate全項目合格
- Golden UAT 12/12合格

## [0.2.0] - 2026-07-17

### Added
- SIMS-Blog-Manager / Generic JSONの自動判定とJSONファイル読込基盤
- Improvement Request Contract v1.0と正規形Schema
- Article ContextモデルとRuntime接続
- 入力検証・正規化・Runtime統合テスト4件

### Changed
- Runtime CLIの既定入力形式を`auto`へ変更
- Runtime成果物に`request_metadata`と`article_context`を追加

### Validation
- Repository Release Gate全項目合格
- Golden UAT 12/12合格

## [0.1.0] - 2026-07-17

### Added
- Product 1.0 Implementation Phaseの初期Repository Baseline
- Repository一括テスト用 `pyproject.toml` と `requirements.txt`
- 実装済みCTR Improvement Vertical Slice
- Runtime、Contract、Knowledge、Decision、Pattern、Quality、Golden UAT資産

### Fixed
- Contract Example Testがpytest collection時に終了する問題を修正
- READMEとVERSIONの不整合を解消

### Release Gate
- `python -m pytest` が成功すること
- CTR Vertical Slice CLIが正常終了すること
- ZIP内に `.git`、`__pycache__`、生成ログを含めないこと

## Pre-implementation history


## [0.13.0-alpha.1] - 2026-07-17

### Added
- CTR Improvement Vertical Slice
- SBM JSONからDecision、Pattern、Draft、Quality、Publication Packageまでの実行CLI
- CTR改善用の決定論的最小生成器とUAT
- ADR-0017

## [0.12.0-alpha.1] - 2026-07-17

### Added

- SIMS-Core Migration Framework v1.0
- 暫定Migration Inventory 10件
- Lessons Learned 12件
- Keep / Adapt / Archive / Remove評価領域
- Migration ValidatorとTest
- ADR-0016

### Note

最新版SIMS-Core Repository ZIPは本Package作成時点で取得できていないため、原本ファイルの完全移行ではなく、確認可能な資料を基にした移行基盤と暫定評価を収録。

# 0.9.0-alpha.1

## Added
- Executable Quality Validation Runtime for all 42 canonical rules
- 13-dimension scoring and 7-gate evaluation
- Explicit unable_to_verify state
- ADR-0013 and runtime tests

# Changelog

## [0.11.0-alpha.1] - 2026-07-17

### Added
- 12-category Golden Dataset
- End-to-End UAT runner and report
- Fixed expected Publish Decision checks
- Mandatory and forbidden output assertions
- Model-Assisted Review fixture connection
- ADR-0015 Golden Dataset as Release Gate


## [0.8.0-alpha.1] - 2026-07-17

### Added
- Provider-neutral Model Adapter Protocol
- Claude Messages / OpenAI Responses / Generic Chat transports
- Context Builder, Prompt Renderer, JSON Output Parser
- Fixture Transport and end-to-end model adapter tests
- ADR-0012 Provider-Neutral Model Adapter

### Changed
- Runtime Orchestrator accepts generic ProductionAdapter and produces structurally validated publication packages.


## [0.7.0-alpha.1] - 2026-07-17

### Added
- Runtime Core with 11-stage decision-aware pipeline.
- Orchestrator, execution state, runtime manifest, asset version locking.
- Generic JSON and SIMS-Blog-Manager input adapters.
- Manual model adapter and deterministic dry-run publication package.
- Runtime validators, end-to-end tests, examples, and ADR-0011.

## [0.6.0-alpha.1] - 2026-07-17

### Added
- Initial Pattern Library 61 definitions
- 8 Pattern Sets and registries
- Decision-to-Pattern mapping policy
- Pattern validation and reference tests
- ADR-0010 Decision-Gated Pattern Selection

## [0.5.0-alpha.1] - 2026-07-17

### Added

- Decision Framework v1.0
- Decision Domain and runtime stage
- 12 initial Decision Definitions
- Decision Context, Decision Record, Action Plan contracts
- Decision Registry and validation tooling
- ADR-0009: Decision Layer Between Knowledge and Pattern

### Changed

- Product Core expanded from four pillars to five pillars
- Runtime flow updated to place Decision before Pattern Selection
- Product specification updated with Decision requirements

## [0.4.0-alpha.1] - 2026-07-17

### Added
- 28 initial Knowledge Items
- 10 Knowledge Sets
- Source, Knowledge, and Knowledge Set registries
- Source, confidence, review, and assembly policies
- Knowledge validation tool

## 0.3.0-alpha.1 - 2026-07-17

### Added
- 13 Quality Dimensionsに対応する初期42 Quality Rules
- 7 Quality Gates
- Rule/Gate Registry
- Quality Asset Validatorとテスト
- Scoring、Checklist、Report仕様

## 0.2.0-alpha.1
- 初期Contract Schema Package

## [0.10.0-alpha.1] - 2026-07-17

### Added
- Targeted Refinement Engine and Issue Router
- Safe deterministic fixes for placeholders, repetitive text, AI-like phrases, and heading hierarchy
- Revision records, action plans, resume-stage routing, and revalidation loop
- ADR-0014 Targeted Refinement Before Regeneration
