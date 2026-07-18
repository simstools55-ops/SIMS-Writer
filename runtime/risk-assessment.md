# Risk Assessment Specification v1.0

## 1. 目的

改善によって既存成果を損なう可能性を評価する。

## 2. リスク要因

### Performance Risk

- 高順位記事のタイトル変更
- 高CTR記事のスニペット変更
- 上位クエリを外す変更

### Content Risk

- 独自体験の削除
- 条件表現の削除
- 具体例の一般化
- 既存の正しい説明を短縮

### Structural Risk

- H2順序の大幅変更
- URL変更
- 内部リンク削除
- FAQ大量追加

### Evidence Risk

- 根拠未確認の新情報追加
- 強い断定追加
- 年度だけ更新
- 古い情報との混在

## 3. 判定

### LOW

- L0〜L2
- S0〜S2
- Preservation 60未満
- performance保護要素への変更なし

### MEDIUM

- L3
- S3
- タイトルまたは導入を変更
- Preservation 75以上
- 複数箇所を変更

### HIGH

- L4〜L5
- S4〜S5
- S/Aランク記事
- 高CTRタイトル変更
- 改善後28日未満
- 独自コンテンツ削除
- Change Budget超過
- 根拠未確認の新しい中心主張

## 4. 高リスク時の処理

- protected_elementsを明示
- 変更理由を具体化
- 変更範囲を再縮小
- Quality Gateで再審査
- 必要に応じてwarningを出力
- 全面書き換えは候補扱いとし、自動確定しない

## 5. blocking risk

次の場合はQuality Gateで停止候補。

- critical誤情報を解消できていない
- 根拠未確認の医療・法律・金融主張
- main_queryを失うタイトル変更
- ArticleID/URL不一致
- Before/After対象不一致
- 予算100%超過相当の変更
