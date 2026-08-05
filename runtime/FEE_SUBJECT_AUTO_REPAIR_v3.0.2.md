# Fee Subject Auto Repair v3.0.2

## Purpose

「無料」「手数料なし」「手数料はいくら」のような料金表現で、支払主体・受取主体・料金種別が曖昧な場合に、利用者へ修正を戻さずWriter内部で公開可能な説明へ直す。

## Required decomposition

1. 誰が支払うか
2. 誰へ支払うか
3. 何の料金か（利用料、予約手数料、サービス料、送客手数料、税等）
4. 外部遷移先で別費用が発生しうるか

## Auto repair scope

SEOタイトル、H1、メタ、導入、H2、FAQ、本文、JSONを横断する。修復後はQF-FAC-006、QF-COM-004、QF-PUB-005を再評価する。

## Finalization rule

安全な局所修正が可能な場合は `AUTO_REPAIR_REQUIRED` を内部状態として処理し、利用者には修復後の `PUBLIC_OK` 成果物だけを提示する。
