# 利用者向け回答Template v3.3.2-RC1

冒頭に公開可否を一文で表示する。

## 今回やること
Doctor Referralを含め、利用者が実作業を始められる説明を1〜3文で示す。Machine Layerの内部項目名は禁止。

## SERP比較結果
SERPが修正判断の根拠になった場合のみ表示する。

## 公開OK（そのままコピペ可能）

PUBLIC_OK変更を1件ずつ、必ず以下の5項目で表示する。Doctor Referralでも省略禁止。

### 変更箇所名
**Before**
> 完全な変更前テキスト

新規追加の場合：
> （該当箇所なし・新規追加）

**After**
> 完全な変更後テキスト

**理由**
平易な日本語で短く説明する。

**期待する効果**
読者側の改善点を平易に説明する。順位上昇などを断定しない。

## 利用者判断
該当時のみ表示。

## 今回変更しないもの
必要時のみ自然な日本語で表示する。`blocked_scope`等の内部名を出さない。

## 次の作業
SBM登録など、利用者が次に行う操作を示す。

内部リンク全件不採用時は「今回は追加できる内部リンクはありません。」だけを表示する。

表示禁止：`doctor_referral`、`allowed_scope`、`blocked_scope`、`actions_permitted`、`actions_prohibited`、Contract内部、Routing、Confidence数値、Evidenceコード、Validation、QA verdict。

最後にContract 4.2 JSONを1ブロックだけ出力し、その後に文章を付けない。
