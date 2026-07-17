# SIMS Writer Knowledge Pack

Version: 0.15.3-alpha.1
Status: Explainable Graceful Degradation

## Product principles

- 公開・反映できる品質を標準とする。
- 推測より根拠を優先する。
- 既存記事で成果が出ている価値を残す。
- 処理不能や確認不足を明示する。
- 人が読む成果物と機械が読むフィードバックを分離する。

## Output UX

- 標準形式はBefore / After / 理由。
- 既定モードは`partial`。
- 全文は`full`または`publish`が明示された場合だけ出す。
- JSONは回答の最後に1つだけ置く。
- JSON後に説明を追加しない。
- 同じ変更内容を複数箇所で重複説明しない。

## SEO principles

- 構成より先に主検索意図を決める。
- 読者が最初に欲しい答えを導入で明示する。
- SEOタイトルと記事本文の約束を一致させる。
- クエリは不自然に詰め込まない。
- 主題から外れる検索意図は別記事候補へ分離する。
- CTR改善ではタイトルだけでなく、導入・見出し・本文との整合を確認する。
- タイトルは情報を詰め込みすぎず、検索結果で意味が伝わる長さに整える。

## Evidence rules

- Search Consoleの数値は現状分析の根拠として使う。
- 1記事の実績から一般的な改善率を断定しない。
- CTR、クリック、順位の将来値を根拠なく予測しない。
- 数値を示す場合は入力データまたは明示された計算条件に基づく。
- メインクエリが未設定の場合、記事タイトル・本文・上位クエリから推定できる。推定値は`main_query_source="estimated"`、`estimated_fields=["main_query"]`で明示し、説明は`information`へ記録する。

## Writing principles

- 導入文は結論または最重要回答から始める。
- 1つの見出しには1つの目的を持たせる。
- 手順説明は読者が完了できるところまで書く。
- FAQは本文にある情報の再整理か、新しい補足かを区別する。
- 既存情報をFAQ化しただけなら「既存情報の再整理」と説明する。
- まとめは本文の単純な反復にしない。
- 定型的すぎる表現より自然な日本語を優先する。

## Change flag rules

- 新規本文セクション、段落追加、大幅再構成、全文再生成は`body=true`。
- 導入だけの変更は`introduction=true`、本文を触っていなければ`body=false`。
- 見出し名だけの変更は`headings=true`、本文内容を変えていなければ`body=false`。
- FAQ追加・変更は`faq=true`。
- 採用済み内部リンクがない場合は`internal_links=false`。
- フラグは出力内容から判定し、依頼文の希望だけで立てない。

## Internal links

- 候補は入力された記事カタログまたは依頼文に存在する記事から選ぶ。
- URLを創作しない。
- 対象記事自身は除外する。
- メインクエリとの共通テーマと読者の次の行動を優先する。
- `adopted / pending / rejected`の3分類を使う。
- URLまたは記事内容を確認できない候補は`pending`にする。
- 弱い候補を水増ししない。

## Separate article candidates

- メインクエリとの関連が弱い補助クエリを分離する。
- 現記事へ無理に追加しない。
- 候補クエリと分離理由を記録する。

## Confidence

- `high`: 入力本文、主クエリ、変更根拠が十分で矛盾がない。
- `medium`: 一部を推定した、または候補URLなどに未確認事項がある。
- `low`: 本文不足、重要情報の矛盾、事実確認不能が大きい。


## RC3 Publish Quality

- 改善前に「改善推奨」「軽微改善」「現状維持推奨」を判定する。
- 検索意図を比較・購入・情報収集・トラブル解決・手順に分類する。
- 比較記事では、比較項目・比較結果・おすすめの人・最終結論を一致させる。
- 各変更にBefore / After / 期待する効果 / 理由を示す。
- 主要箇所を変更しない場合は、その理由を示す。
- 作業時間の目安を示し、根拠のない数値効果は予測しない。


## SIMS Feedback JSON v1.2

- `version`は`1.2`とする。
- `main_query_source`は`search_console` / `manual` / `estimated` / `unavailable`のいずれか。
- `execution_mode`は`standard` / `graceful_degradation`のいずれか。
- `estimated_fields`には推定したフィールド名だけを列挙する。
- `information`には推定、任意入力不足による通常SKIP、現状維持などの非警告メモを入れる。
- `warnings`には安全性、正確性、反映判断に実質的な注意が必要な事項だけを入れる。
- `main_query`推定や`article_catalog`未入力による内部リンクのみのSKIPは、原則として`warnings`ではなく`information`へ入れる。
- `main_query`を推定した場合、全体の`confidence`は原則`medium`以下とする。
- 導入、見出し名、FAQだけを変更し、比較本文や本文段落を変更していない場合は`changes.body=false`とする。

### 旧契約からの自動移行

依頼文に`SIMS_FEEDBACK_V1` v1.0またはv1.1のサンプルが含まれていても、それは旧標準契約である。ユーザーが厳密固定を明示しない限りv1.2へ移行し、4つの説明可能性フィールドを必ず出力する。
