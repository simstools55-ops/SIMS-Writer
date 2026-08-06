# Output Separation Policy v2.0

出力を次の3層へ分離する。

1. User Publication View: 公開OKと利用者判断だけ。
2. SBM Feedback Contract 3.0: 反映結果と再測定情報。
3. Internal Audit Record: 診断、Coverage、Validation、QA、SWLS、却下案。

内部情報を通常利用者向け文章またはContract 3.0へ混入させてはならない。


## SERP gate consistency
A final response is invalid when it states that current top results were not inspected while publishing heading, FAQ, body, structural, competitor-gap or title-promise changes. Publication QA must reject this combination before user output. Internal-link candidate rejection may still be summarized in one sentence; candidate-by-candidate rejection belongs to internal audit.
