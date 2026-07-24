# Coverage Pattern Library v1.0

## 1. How-to型

Required候補：

- できるか
- 前提条件
- 手順
- つまずきやすい点
- できない場合
- 結果確認

## 2. 料金・コスト型

Required候補：

- 結論
- 月額・年額
- 計算条件
- 価格差の理由
- 節約方法
- 注意点

## 3. 比較型

Required候補：

- 比較対象
- 比較軸
- 違い
- 向いている人
- 結論
- 選び方

## 4. トラブル解決型

Required候補：

- 症状
- 原因候補
- 優先順位
- 解決手順
- 解決しない場合
- データ消失等の注意

## 5. 用語・意味型

Required候補：

- 一言での意味
- 具体例
- 使われる場面
- 類似語との違い
- 注意点

## 6. 年度・運勢・季節型

Required候補：

- 対象期間
- 結論
- 条件
- 月別または時期別
- 更新時点
- 古い情報との差

## 7. 製品レビュー型

Required候補：

- 使用条件
- 良かった点
- 気になった点
- 向いている人
- 向かない人
- 仕様と体験の区別

## 8. 使用制約

このPattern LibraryはArticle Type Routerではない。

Phase Aでは、検索意図から期待論点を補助生成するためだけに使う。


## v1.3.0 Hardening

Query Coverageは常時表示し、Primary／Secondary／Adjacent／Separate Articleへ分類する。Coverage Confidenceをhigh／medium／lowで示す。高CTR語句、完全一致クエリ、エラー文、固有名詞はWinner Query Preservation対象とする。複数意図が競合する場合はQUERY_MIXを検討する。warningは公開判断へ影響する事項に限定し、それ以外はinformationとする。
