# Article Evaluation Workflow v1.0

## 1. 入力の正規化

記事ごとの依頼文と回答を、共通評価フォーマットへ変換する。

推測で不足項目を補完しない。不明項目は`NOT_AVAILABLE`とする。

## 2. 期待値の作成

SIMS Writer回答を評価する前に、評価者側で以下を仮判定する。

- primary diagnosis
- protect/change対象
- expected rewrite level
- expected rewrite scope
- expected gate decision

回答を見てから期待値を変えない。

## 3. 差分評価

```text
Expected
vs
Actual
```

を比較する。

評価軸：

- diagnosis
- preservation
- change budget
- level
- scope
- risk
- gate
- output completeness

## 4. 許容差

### Preservation Score

±10点を通常許容。

ただしスコア帯が変わり、変更上限へ影響する場合は欠陥候補。

### Change Budget

±10ポイントを通常許容。

ただし良好記事で30%以上となる場合は過剰修正候補。

### Rewrite Level

原則±1レベル。

次は重大差異。

- Expected L1、Actual L4/L5
- Expected L4、Actual L0/L1
- LOW_SAMPLEでL4/L5
- PROTECT_WINNERでL4/L5

### Rewrite Scope

原則±1スコープ。

L1/S5などの不自然な組み合わせは欠陥。

### Quality Gate

- PASSとPASS_WITH_WARNINGの差は軽微の場合あり
- PASS系とREVIEW_REQUIREDの差は要分析
- BLOCK見逃しは重大
- 誤BLOCKは重大

## 5. 変更内容評価

変更量だけでなく、変更対象の妥当性を見る。

良い変更：

- 問題箇所だけを直す
- 強い部分を保護
- 不足論点を局所追加
- 変更理由が検索診断と一致

悪い変更：

- 文体をAI風に統一
- 元記事の個性を削除
- 関係ない見出しを追加
- 主クエリを弱める
- 高CTRタイトルを根拠なく変更
- FAQだけで本文不足を補う

## 6. 最終所見

記事ごとに必ず以下を1〜3文で記録する。

- 良かった判断
- 最も重要な問題
- 次の記事で観察すべき点
