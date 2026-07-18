# SIMS Writer Validation Layer v1.0

## 目的

Validation Layerは、記事改善案とSIMSフィードバックJSONを公開・登録する前に検査する最終品質防壁である。
10記事実記事テストで確認された再発問題を、モデルの自己判断ではなく明示的な検証項目として固定する。

## 実行順序

1. Input Integrity
2. Search Intent Alignment
3. Preservation Integrity
4. Change Budget
5. Presentation Completeness
6. Factuality and Evidence
7. JSON Contract
8. Language and Leakage
9. Final Gate Decision

## 判定

- `PASS`: 重大違反なし、警告なし
- `PASS_WITH_WARNING`: 公開を妨げない警告のみ
- `FAIL`: 重大違反が1件以上
- `UNVERIFIABLE`: 必要情報不足で検証不能

## 重大違反

- ArticleIDまたはURLの不一致
- 検索意図の変更
- 保護対象の削除・改変
- Change Budgetの超過
- 事実未確認の数値・比較・断定
- Before/Afterの対応欠落
- JSON Schema不適合
- 英文分析、内部思考、別記事情報の混入

## 必須保護対象

- 広告コード
- アフィリエイトリンク
- 実体験・独自レビュー
- 比較表
- 独自画像と画像説明
- CTA
- 既存のまとめ・結論

## 文字数規則

- SEOタイトル: 原則45文字以内
- メタディスクリプション: 原則80〜140文字

文字数だけを理由に検索意図や自然な日本語を損なってはならない。

## LOW_SAMPLE

LOW_SAMPLEでは、改善案を出しても効果断定を禁止する。`PASS_WITH_WARNING`とし、原則28日後の再測定を添える。

## POSITION_OPPORTUNITY

順位6〜12位かつCTRに改善余地がある場合は、タイトル・導入・見出し・FAQの局所改善を優先する。全文リライトは自動選択しない。
