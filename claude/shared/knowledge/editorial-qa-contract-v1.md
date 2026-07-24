# SIMS Editorial QA Contract v1

## 共通判定

- PASS
- PASS_WITH_WARNING
- PASS_WITH_MINOR_FIX
- PASS_WITH_REQUIRED_FIX
- FAIL

## 共通原則

- 作成担当と評価担当を論理分離する。
- QAは安全な局所修正のみ行う。
- 修正前後と判定履歴を保存する。
- 最大再評価回数を制限する。
- 保護対象を変更しない。
- Required Fixが残る成果物を公開可能としない。

## 製品別Adapter

WriterはWinner Query、既存記事保全、Before/Afterを追加評価する。Creatorは新規記事のEvidence、構成、HTML完成度を追加評価する。共通Contract自体には製品固有フィールドを必須化しない。
