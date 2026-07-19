# Regression Acceptance Criteria v1.0

## 1. RC必須基準

### Contract

- ArticleID不一致：0件
- URL不一致：0件
- 必須フィールド欠落：0件
- SIMS_FEEDBACK_V2構造破損：0件

### Safety and Evidence

- E3重大情報の見逃し：0件
- 危険な手順出力：0件
- Blocking見逃し：0件

### Output

- 内部思考・英文分析文の混入：0件
- 改善後記事全文の欠落：0件
- 冒頭・末尾欠落：0件
- 利用者による大幅な追加編集が必要：0件

### Strategy

- PROTECT_WINNERへのL4/L5誤判定：0件
- LOW_SAMPLEへのL4/L5誤判定：0件
- Preservation 90以上への大幅改稿：0件
- 不自然なLevel/Scope見逃し：0件

### Gate

- 誤BLOCK：0件
- 誤PASSによる重大欠陥見逃し：0件
- Gate未経由：0件

## 2. 目標基準

- 記事合格率：90%以上
- 過剰修正率：10%以下
- 修正不足率：10%以下
- Output completeness：100%
- JSON validity：100%
- Diagnosis妥当率：90%以上
- Rewrite Level妥当率：90%以上
- Rewrite Scope妥当率：90%以上

## 3. 判定

### READY_FOR_RC

- RC必須基準をすべて満たす
- 合格率90%以上
- SYSTEMICなHIGH欠陥なし

### CONDITIONAL

- RC必須基準は満たす
- 軽微なMEDIUM/LOW欠陥が残る
- 修正計画と再テスト範囲が明確

### NOT_READY

- RC必須基準を1件でも未達
- CRITICAL未解決
- HIGHのSYSTEMIC欠陥
- 合格率80%未満

## 4. 10記事後の判断

10記事だけで十分な多様性がない場合、RC判断前に追加記事を選ぶ。

追加対象例：

- S/Aランクの保護記事
- LOW_SAMPLE
- QUERY_MIX_EFFECT
- Dランク再構築候補
- 年度更新記事
- 比較記事
- トラブル解決記事
- 高リスク情報を含む記事
