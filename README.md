# SIMS Writer v1.0.0 Baseline

Google Search Console等の実データをもとに、既存記事を壊さず局所改善するための品質・契約・Knowledge・Pattern中心のリライトシステムです。

## v1.0.0の位置付け

- 実記事回帰テスト5件：PASS 3件、PASS_WITH_WARNING 2件、FAIL 0件
- v0.2.3 Validation Hotfixを運用ベースラインとして固定
- SWLS（SIMS Writer Learning System）Betaを追加

## 主な構成

- `claude/`：Claude Project用資産
- `contracts/`：入出力契約
- `knowledge/`：診断・品質・保護ルール
- `runtime/`：評価・Validationパイプライン
- `patterns/`：改善パターン
- `learning/`：運用データ、利用者コメント、効果測定、10記事レポート
- `tests/`：回帰テストとベースライン

SWLSの使い方は[`learning/README.md`](learning/README.md)を参照してください。
