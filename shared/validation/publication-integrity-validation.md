# Publication Integrity Validation

FAIL conditions:

- 変動情報を現在の一次情報なしでPUBLIC_OKへ入れる
- 機能の不存在、期間、頻度、最安値を未検証で断定する
- 不確実な主張をFAQだけ修正し、CTA・導入・本文に残す
- リンク保護を理由にCTAを検証対象外とする
- 質問と回答が一致しないFAQを公開する
- 局所修正後の表示文とJSONが一致しない
- article title本体とサイト名付き最終SEOタイトルの長さを混同する

Required audit order:

1. dynamic claims
2. marketing claims
3. affiliate CTA
4. FAQ
5. cross-component search
6. final JSON synchronization

## v2.4 Real-article integrity extension

`validation/real-article-publication-validation.md` を最終ゲートとして追加する。
特に、実記事由来ではないBefore、要約After、前回提案文の混入、表示文とJSONの非同期はFAILとする。
