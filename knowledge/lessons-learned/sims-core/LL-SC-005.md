---
id: LL-SC-005
title: 品質基準をPromptだけに置かない
source_product: SIMS-Core
classification: adapt
status: review
version: 1.0.0
reviewed_at: 2026-07-17
---

# 品質基準をPromptだけに置かない

## 観察

重要なルールがProject InstructionsとEngineへ重複し、更新時の不整合が起こりやすい。

## SIMS Writerでの判断

Knowledge、Quality Rule、ContractをCanonical Assetとし、PromptはRuntime Viewを描画する。

## active化条件

関連するKnowledge・Decision・Pattern・Quality Rule・Golden Caseとの対応を確認し、重複がないこと。
