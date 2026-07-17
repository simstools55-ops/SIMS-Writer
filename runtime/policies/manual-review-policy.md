# Manual Review Policy

`manual_review_required`は、安全性、YMYL相当の重大判断、重大な事実確認不足、出力契約の解消不能な競合、Blocker残存など、人手確認なしでは成果物を安全に提示できない場合に限定します。

次の不足だけでは処理全体を停止しません。

- `main_query`不足：タイトル等から推定し、推定不能ならクエリ依存処理だけを保留してWarning
- `article_catalog`不足：内部リンク候補選定だけをSKIP
- 外部Source取得不能：既存入力で改善可能な項目を継続しWarning

任意入力や補助データの不足はGraceful Degradationで処理し、fatal errorへ昇格させません。
