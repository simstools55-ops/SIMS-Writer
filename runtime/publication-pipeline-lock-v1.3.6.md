# SIMS Writer v2.0.0 RC2 Publication Pipeline Lock

この文書は旧Publication Pipeline Lock、旧Contract例、旧出力Templateより常に優先される。

## 固定パイプライン

`Strategy → Evidence → Editing → Publication Decision → Visibility Filter → Contract Validation → Output`

- Strategyは公開可否を決めない。
- Evidence判定は後段から上書きできない。
- `MULTIPLE_THIRD_PARTY`の変動仕様は`PUBLIC_OK`禁止。
- `INTERNAL_REJECT`は出力禁止。

## 最終出力ゲート

出力直前に次をすべて検査する。

1. Evidence違反がない。
2. USER_DECISIONに送るべき変更がPUBLIC_OKへ混入していない。
3. 通常表示に内部診断・QA・SWLS・Evidence詳細・内部リンク不採用一覧がない。
4. JSONがContract 4.0 Schemaに適合する。
5. JSONの`contract_version`が`4.1`である。
6. `publication_result`外に旧契約フィールドがない。
7. Before/Afterが省略記号ではなく、利用者が反映できる完全な内容である。

一つでも違反があれば出力せず、内部で修正して再検査する。
