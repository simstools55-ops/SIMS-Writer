---
id: LL-SC-002
title: 内部分析を利用者出力へ漏らさない
source_product: SIMS-Core
classification: keep
status: review
version: 1.0.0
reviewed_at: 2026-07-17
---

# 内部分析を利用者出力へ漏らさない

## 観察

実運用で英語の内部分析が表示される事象が確認された。

## SIMS Writerでの判断

内部推論、Adapterログ、Quality判定理由をPublication Outputから分離する。

## active化条件

関連するKnowledge・Decision・Pattern・Quality Rule・Golden Caseとの対応を確認し、重複がないこと。
