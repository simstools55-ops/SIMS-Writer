# Claude Output Contract

Claude Projectが返す記事改善JSONをRuntimeへ受け入れる前に検証する契約です。

- JSON Schemaによる構造検証
- `generated`時の完成記事必須化
- `manual_review_required`時の未解決事項必須化
- 入力記事カタログにない内部リンクURLの拒否
- 補助クエリに存在しない別記事候補の警告
