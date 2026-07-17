# Claude Project Golden UAT

Claude Projectの出力揺れと安全動作を、固定ケースで検証するためのテスト資産です。

- 正常な完成記事
- Markdownコードフェンス付きJSON
- camelCaseキーや軽微な空白の正規化
- 本文不足時の手動確認
- 未登録URLの拒否
- 本文なし完成記事の拒否

実行:

```bash
python -m runtime.sims_writer_runtime.cli --output claude-uat-output --run-claude-uat
```
