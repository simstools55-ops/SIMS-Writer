# Defect Classification v1.0

## 1. Severity

### CRITICAL

- 誤った記事へ変更
- ArticleID/URL不一致
- 危険な高リスク情報
- 内部思考や秘密情報の露出
- JSON構造破損
- Blocking見逃し

### HIGH

- 全面改稿の重大誤判定
- PROTECT_WINNERの破壊
- 検索意図の変更
- 本文大幅欠落
- 改善後記事全文の欠落
- Before/After対象不一致

### MEDIUM

- 局所的な過剰修正
- 必須論点の不足
- Evidence判断の不足
- Change Budgetの不整合
- Warning不足
- 内部リンク提案の不整合

### LOW

- 表記
- 軽微な説明不足
- 冗長
- ラベルや順序の軽微問題

## 2. Defect Type

### CONTRACT

- D-CON-001 ArticleID不一致
- D-CON-002 URL不一致
- D-CON-003 必須項目欠落
- D-CON-004 Before/After不一致
- D-CON-005 JSON不整合

### DIAGNOSIS

- D-DIA-001 診断タイプ誤り
- D-DIA-002 LOW_SAMPLE誤解
- D-DIA-003 QUERY_MIX_EFFECT見逃し
- D-DIA-004 HEALTHY記事の過剰改善
- D-DIA-005 改善必要記事の見逃し

### CONSISTENCY

- D-CNS-001 年度矛盾見逃し
- D-CNS-002 数値矛盾見逃し
- D-CNS-003 FAQ/本文矛盾
- D-CNS-004 タイトル/本文矛盾
- D-CNS-005 Entity不統一

### EVIDENCE

- D-EVI-001 強い断定見逃し
- D-EVI-002 根拠不要箇所への過剰要求
- D-EVI-003 E3未確認見逃し
- D-EVI-004 体験談の一般化
- D-EVI-005 古い根拠採用

### COVERAGE

- D-COV-001 必須論点不足
- D-COV-002 過剰網羅
- D-COV-003 検索意図逸脱
- D-COV-004 FAQ依存
- D-COV-005 重複追加

### STRATEGY

- D-STR-001 Preservation過小
- D-STR-002 Preservation過大
- D-STR-003 Change Budget過大
- D-STR-004 Change Budget過小
- D-STR-005 Rewrite Level過大
- D-STR-006 Rewrite Level過小
- D-STR-007 Rewrite Scope不整合
- D-STR-008 protected_elements欠落
- D-STR-009 Risk誤判定

### GATE

- D-GAT-001 誤PASS
- D-GAT-002 誤BLOCK
- D-GAT-003 Review不足
- D-GAT-004 Warning不足
- D-GAT-005 Gate未経由

### OUTPUT

- D-OUT-001 英文思考混入
- D-OUT-002 冒頭欠落
- D-OUT-003 末尾欠落
- D-OUT-004 全文欠落
- D-OUT-005 内部リンク形式不足
- D-OUT-006 日本語品質不足
- D-OUT-007 利用者の追加編集が必要

## 3. Root Cause Layer

- Project Instructions
- Runtime
- Knowledge
- Contract
- Pattern Library
- Test Coverage
- Model Variance
- Input Quality

## 4. 再発判定

同一Defect Typeが2記事以上で発生：

```text
RECURRENT
```

3記事以上またはCRITICAL/HIGHが再発：

```text
SYSTEMIC
```

SYSTEMICはRC阻害要因。
