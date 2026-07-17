# RC2 Claude Test Checklist

- [ ] 回答は日本語のみ
- [ ] 内部思考・英語分析が表示されない
- [ ] Before / After / 理由が対応している
- [ ] `partial`で全文を出していない
- [ ] 本文追加時に`changes.body=true`
- [ ] `main_query`はクエリ文字列のみ
- [ ] 推定注記は`warnings`にある
- [ ] 根拠のないCTR・クリック予測がない
- [ ] 未確認URLを`adopted`にしていない
- [ ] `article_content`を使用していない
- [ ] JSONは最後に1つだけ
- [ ] JSON後に文章がない

## v0.14.2 Quality Patch

- [ ] 成果物の前に挨拶・了承文・利用者への呼称がない
- [ ] SEOタイトルが45文字以内（40文字以内推奨）
- [ ] メタディスクリプションが140文字以内（120文字以内推奨）
- [ ] JSONは `json` 言語指定付きコードブロックで1つだけ
- [ ] JSONコードブロックの後に文章がない
- [ ] partialは正式主力、full/publishはベータとして扱われている


## Strict Contract Compliance UAT

- ユーザー提示JSONの最上位キーが同名・同順序である
- 入れ子キーが同名・同順序である
- 文字列・真偽値・配列・オブジェクトの型が一致する
- 必須項目の欠落が0件である
- 契約外フィールドが0件である
- `format`を`schema`へ変更していない
- `description`を`meta_description`へ変更していない
- JSONは回答末尾の単一`json`コードブロックである
