---
id: LL-SC-009
title: Engineの価値は名前ではなく判断知識にある
source_product: SIMS-Core
classification: adapt
status: review
version: 1.0.0
reviewed_at: 2026-07-17
---

# Engineの価値は名前ではなく判断知識にある

## 観察

Engine分割は開発初期の整理に役立ったが、責務重複と巨大化を招いた。

## SIMS Writerでの判断

EngineからDecision、Pattern、Quality Rule、Contractを抽出し、Engine構造は継承しない。

## active化条件

関連するKnowledge・Decision・Pattern・Quality Rule・Golden Caseとの対応を確認し、重複がないこと。
