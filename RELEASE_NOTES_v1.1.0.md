# SIMS Writer v1.1.0 Release Notes

## Release status

正式版（Production Release）

## Implemented capabilities

1. Intent Gap Detection
2. Hidden Anxiety Detection
3. SERP Entity Preservation
4. Semantic Internal Link Evaluation
5. FAQ Evolution
6. Conditional Editorial Opinion
7. Evidence Transparency

## Priority B implementation

- Validation rules VAL-017〜VAL-023を正式採用
- Pattern Libraryへ7能力の適用パターンを接続
- Runtime `editorial_signals`を7能力対応へ拡張
- Shared Knowledge v1.1.0回帰テストを追加
- Writer／Claude Shared Snapshotの一致検証を追加

## Compatibility guarantees

- Preservation思想を維持
- Preservation Scoreを変更しない
- Change Budgetを変更しない
- Rewrite Level／Rewrite Scopeを変更しない
- SIMS Feedback JSON Contractを変更しない
- Product 5.3.1識別情報を透過保持
- 旧入力形式を継続受理

## Shared Knowledge

SIMS-Shared-Editorial-Knowledge v1.1.0を唯一の正本とし、WriterおよびClaude配布物には検証済みスナップショットを収録する。
