# SIMS Writer v1.1.0

Google Search Console等の実データをもとに、既存記事を壊さず局所改善するための品質・契約・Knowledge・Pattern中心のリライトシステムです。

## v1.1.0の位置付け

- 実記事で有効性を確認した7つのEditorial Capabilityを正式実装
- Preservation、Change Budget、Rewrite Level/Scope、JSON Contractを維持
- Shared Editorial Knowledge v1.1.0を唯一の正本としてスナップショット連携
- Product 5.3.1識別情報と旧入力形式の後方互換を維持

## 主な構成

- `claude/`：Claude Project用資産
- `contracts/`：入出力契約
- `knowledge/`：診断・品質・保護ルール
- `runtime/`：評価・Validationパイプライン
- `patterns/`：改善パターン

- `shared/`：`SIMS-Shared-Editorial-Knowledge v1.1.0`の検証済み・編集禁止スナップショット
- `learning/`：運用データ、利用者コメント、効果測定、10記事レポート
- `tests/`：回帰テストとベースライン

SWLSの使い方は[`learning/README.md`](learning/README.md)を参照してください。

## Shared Knowledge dependency

SIMS Writerは、独立製品`SIMS-Shared-Editorial-Knowledge`を正本として利用します。実行時の外部取得は行わず、リリースで検証済みスナップショットを`shared/`へ同梱します。Writer側の`shared/`は直接編集しません。
