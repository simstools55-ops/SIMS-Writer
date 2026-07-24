# Self QA Runtime Instructions v1.1

改善案のBefore/AfterとSIMS Feedbackを作成後、公開前QAを必ず実行する。

1. 初回判定を記録する。
2. PASSまたはPASS_WITH_WARNINGなら文章を再生成しない。
3. MINOR_FIX相当は許可済みの局所修正だけを行う。
4. Winner Query、体験談、広告、比較表、根拠のない事実は自動変更しない。
5. 修正後に再評価する。最大2回。
6. Required FixまたはFAILが残る場合は公開OKと表示しない。
7. 最終出力には公開判定と、修正済みの最終版だけを明確に示す。

QA Contractは`SIMS_EDITORIAL_QA_V1`。Writer固有の出力Contractとは分離して扱う。
