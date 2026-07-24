---
id: LL-SC-003
title: 不足情報を推測で埋めない
source_product: SIMS-Core
classification: keep
status: review
version: 1.0.0
reviewed_at: 2026-07-17
---

# 不足情報を推測で埋めない

## 観察

対象記事が確認できない状態でも、クエリデータから記事内容を推測する出力が起きた。

## SIMS Writerでの判断

Unknown、Missing、Unable to Retrieveを区別し、Source取得不能時は明示的に停止する。

## active化条件

関連するKnowledge・Decision・Pattern・Quality Rule・Golden Caseとの対応を確認し、重複がないこと。
