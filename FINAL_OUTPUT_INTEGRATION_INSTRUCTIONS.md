# RC2 Final Output Integration Instructions

利用者向けMarkdownを組み立てた後、内部監査情報を除去し、Contract 4.0 JSONだけを付ける。

禁止：旧Contract 2.1/3.0 JSON、Validation、publication_qa、SWLS、内部リンク不採用一覧、Evidenceコード、診断コード。

EvidenceがUSER_DECISIONなら、その事実を含むすべての修正対象（タイトル・メタ・導入・見出し・FAQ・本文）もUSER_DECISIONへ送る。文章ごとに判定を分裂させてはならない。

standalone `qa_verdict`は外部出力しない。


## Release final mandatory quality gates

Read and apply `runtime/RELEASE_FINAL_QUALITY_GATE.md`. Safety, evidence, expectation alignment and semantic title validation override SEO opportunity.


## v2.1.0 Quality Pattern Library
Before adding or improvising a new quality rule, read `shared/quality/QUALITY_PATTERN_LIBRARY.md` and `shared/quality/OPERATIONAL_LEARNING_PROMOTION_POLICY.md`. Repeated defects must be treated as Mapping or Validation defects, not solved by article-specific prompt growth.
