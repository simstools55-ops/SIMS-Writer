# SIMS Shared Editorial Knowledge v3.5.0

## Human Experience / Presentation Framework

実記事検証で確認された「Machine出力は正しいが利用者が作業できない」UX退化をPlatform共通仕様として修正するBaseline。

### Added
- Human Experience Architecture v1
- Presentation Standard v1
- Human Output Policy v1
- Machine Output Policy v1
- Human Usability Gate v1

### Scope
- 先行実装対象: Doctor / SBM / Writer
- 共通仕様対象: Creator / Mergeを含む全Editorial Platform製品
- Creator / Mergeの動作変更は後続フェーズで行い、本リリースでは共通ルールの参照を正式化する。

### Key regression rule
Doctor Referral TreatmentでもWriterのBefore / After / 理由 / 期待効果を省略してはならない。
