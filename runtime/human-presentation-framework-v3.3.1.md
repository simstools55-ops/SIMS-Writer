# Human Presentation Framework v3.3.1-RC1

Writerは通常改善と`DOCTOR_REFERRAL_TREATMENT`を同じHuman Presentation Standardで表示する。

## 固定表示順

1. 公開可否
2. 今回やること
3. 公開OK変更（対象 / Before / After / 理由 / 期待する効果）
4. 利用者判断（存在時のみ）
5. 今回変更しないもの（必要時のみ）
6. 次の作業
7. `SIMS_FEEDBACK_V2` JSON（最後）

## Doctor Referral

Doctor ReferralはMachine Layerであり、`allowed_scope`、`blocked_scope`、`actions_permitted`、Contract、Routing、Confidence等を通常利用者向け本文へ表示しない。

Doctor Referralで治療範囲が狭くても、PUBLIC_OK変更の表示品質を簡略化してはならない。各変更には必ず完全なBefore/Afterを出す。新規追加で変更前テキストが存在しない場合は`（該当箇所なし・新規追加）`と表示する。

`reason`と`expected_effect`はMachine LayerからHuman Layerへ渡してよい説明情報であり、内部コードではなく平易な日本語にする。
