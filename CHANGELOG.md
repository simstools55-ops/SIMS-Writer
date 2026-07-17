# Changelog

## 0.15.4-alpha.1

- 利用者向け`確認事項`とJSONの`information`の重複を禁止
- 未解決事項がない場合は`確認事項`見出しを省略
- 検索意図をPrimaryと任意のSecondaryで整理する規則を追加
- 変更箇所と距離のある根拠なしの順位改善予測を抑止
- Claude Project出力品質のリリースゲートを追加

## 0.15.3-alpha.1

- Claude ProjectのKnowledge Packを現行版へ同期
- `SIMS_FEEDBACK_V1` v1.0/v1.1サンプルをv1.2へ自動移行する規則を追加
- 推定と通常SKIPを`information`へ分離する指示の矛盾を解消
- Project InstructionsとKnowledge Packのバージョン整合をリリースゲート化

## 0.15.2-alpha.1

- `warnings`と`information`を分離し、通常スキップ・推定・現状維持メモをInformationへ移動
- `main_query_source`を追加し、`search_console` / `manual` / `estimated` / `unavailable`を明示
- `execution_mode`を追加し、通常実行と`graceful_degradation`を区別
- `estimated_fields`を追加し、推定された入力項目を機械判読可能に記録
- SIMS_FEEDBACK_V1をv1.2へ更新し、メタデータ整合性Validatorと回帰テストを追加

## 0.15.1-alpha.1

- `manual_review_required`を人手確認が不可欠な場合だけに限定
- `main_query`欠落時もタイトル等から推定し、推定不能時はWarning付きで処理継続
- `article_catalog`欠落時は内部リンク候補選定だけをSKIP
- 外部Sourceや補助入力の欠落をfatal errorではなくWarningとして扱うGraceful Degradationを実装
- A000008相当の欠損入力回帰テストを追加
- Golden UAT 12件を新しい継続動作へ更新

## 0.15.0-alpha.1

- RC3 Publish Qualityを開始
- 改善推奨・軽微改善・現状維持推奨の3段階判定を追加
- 検索意図分類と比較記事整合性Validatorを追加
- Before / Afterへ期待する効果と変更しない理由のルールを追加
- 編集作業時間の目安を出力へ追加
- RC3回帰テスト6件を追加

## 0.14.3-alpha.1

- ユーザー提示JSON契約をSIMS標準より優先するSchema Lockを追加
- キー名・階層・型・必須項目・順序の厳密検証を追加
- 契約外フィールドの追加を禁止
- Claude Instructionsから競合する旧固定JSON例を撤去
- A000008再UAT用Strict Contractテストを追加

## 0.14.2-alpha.1

- 成果物前の不要な挨拶・了承文・呼称を禁止
- SEOタイトルとメタディスクリプションの推奨値・上限値をValidatorへ追加
- 回答末尾の単一 `json` コードブロックを強制
- `partial` をProduct 1.0の正式な主力モードに位置付け
- `full` / `publish` を構造保持未保証のベータモードに位置付け


## 0.14.1-alpha.1

- Added the missing `claude/` deployment package.
- Updated Claude Project Instructions for RC2 human output plus final JSON.
- Added output-mode, change-flag, internal-link, evidence, and JSON-last rules.
- Added Claude setup guide and RC2 test checklist.
- Corrective release for v0.14.0-alpha.1.

## [0.14.0-alpha.1] - 2026-07-17

### Added
- Output Contract v1.1 and Output Contract Validator
- `summary / partial / full / publish / json_only` output modes
- Human-facing Before/After layer separated from SIMS_FEEDBACK_V1
- Automatic change-flag inference and main-query warning separation
- Internal-link verification and unsupported forecast safeguards
- RC2 regression tests based on eight real-article UAT cases
- ADR-0018

### Changed
- Default CTR output mode is `partial`; article_content is excluded unless full/publish is requested
- README and VERSION aligned to 0.14.0-alpha.1

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
