# Regression Test Procedure v1.0

## 1. テスト準備

各記事について以下を揃える。

- ArticleID
- URL
- 記事タイトル
- SEOタイトル
- メタディスクリプション
- メインクエリ
- Search Consoleデータ
- 記事ランク
- 改善目的
- 変更方針
- 上位クエリ
- 内部リンク候補
- SIMS Writer回答
- 必要に応じて元記事本文

## 2. 記事ごとの評価手順

### Step 1 Contract確認

- ArticleID一致
- URL一致
- 必須項目
- 出力形式
- SIMS_FEEDBACK_V2
- Before/After対応

### Step 2 Search Diagnosis確認

- 診断タイプは妥当か
- LOW_SAMPLEを誤って品質不良扱いしていないか
- 主クエリと記事全体の差を認識しているか
- CTR、順位、表示回数の解釈は妥当か

### Step 3 Consistency確認

- 年度
- 数値
- タイトル
- 導入
- 見出し
- 本文
- FAQ
- まとめ
- 内部リンク

### Step 4 Evidence確認

- 強い断定
- 数値
- 価格
- 製品仕様
- 制度
- 高リスク情報
- 体験談の一般化

### Step 5 Coverage確認

- 検索意図への直接回答
- 必須論点
- 不要な網羅化
- FAQ依存
- 競合模倣
- 検索意図からの逸脱

### Step 6 Improvement Strategy確認

- Preservation Score
- Change Budget
- Rewrite Level
- Rewrite Scope
- Risk
- protected_elements
- change_targets

### Step 7 Quality Gate確認

- PASS系か
- REVIEW_REQUIREDか
- BLOCKか
- 判定は過大・過小でないか
- Warningは行動可能か

### Step 8 出力品質確認

- 日本語のみ
- 内部思考文なし
- 改善サマリー
- Before/After
- 理由
- 内部リンク評価
- 改善後記事全文
- JSON整合

## 3. 記事別判定

- PASS
- PASS_WITH_MINOR_ISSUES
- FAIL

### PASS

重大・軽微を問わず修正不要。

### PASS_WITH_MINOR_ISSUES

公開品質は満たすが、再発防止すべき軽微問題あり。

### FAIL

次のいずれか。

- 誤った改善方針
- 過剰修正
- 修正不足
- Contract違反
- 出力欠落
- 内部思考混入
- Blocking見逃し
- 利用者が追加編集しないと使えない

## 4. 累積記録

記事評価後、必ず次を更新する。

- 累積合格数
- 欠陥コード件数
- Phase別欠陥件数
- 再発問題
- 新規問題
- 修正済み問題
- RC阻害要因

## 5. 再テスト

修正後は、欠陥が発生した記事だけでなく、関連する過去合格記事も再テストする。

例：

タイトル判断を修正した場合：

- CTR_OPPORTUNITY記事
- PROTECT_WINNER記事
- QUERY_MIX_EFFECT記事
- LOW_SAMPLE記事

を再テストする。
