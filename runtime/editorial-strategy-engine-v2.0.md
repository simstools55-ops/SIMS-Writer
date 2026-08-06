# Editorial Strategy Engine v2.0

修正候補を作る前に、`問題 → 原因 → 戦略 → 編集`を内部で固定する。

## 入力
平均順位、表示回数、CTR、検索意図一致、SERP Gap、Evidence、既存記事の完成度。

## 戦略
- `CTR_PRESENTATION`: 上位表示・低CTR。タイトル、メタ、導入を中心にする。
- `SERP_GAP_COMPLETION`: 3位以下かつ根拠のある不足。重要回答を補う。
- `SEARCH_INTENT_REALIGNMENT`: 主意図がずれている。中心回答と構成を再整合する。
- `CONTENT_DEPTH_AND_EVIDENCE`: 深い順位で具体性・根拠が不足。本文を補強する。
- `PRESERVE_AND_MONITOR`: 欠落が弱い。既存資産を保全する。
- `SEPARATE_INTENT_ARTICLE`: 別意図。現記事へ混在させない。

戦略・診断・スコアは利用者へ表示しない。利用者には必要な場合だけ平易な一文を示す。
