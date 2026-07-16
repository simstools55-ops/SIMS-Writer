# Result Artifact Output v1.0

SIMS WriterはRuntime実行結果を一つの巨大JSONだけで終わらせず、用途別の実在ファイルへ分離する。

## Output Set

1. `runtime-result.json`: 監査・再現用の全実行記録
2. `publication-package.json`: 公開判断とSEOメタ情報を含む配布用Package
3. `article.md`: 人が確認・編集できる完成記事
4. `improvement-report.md`: Before / After、判断理由、品質判定
5. `execution-manifest.json`: Execution ID、Request ID、固定資産Version、ファイル一覧

## Principles

- UTF-8で保存する
- 同じ出力先への再実行で中途半端な追記を行わない
- Runtimeの公開判定を成果物側で変更しない
- JSONとMarkdownの役割を分離する
