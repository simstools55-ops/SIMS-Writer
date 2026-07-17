# Claude Project 実装手順 — User Test RC1

## 1. 新しいProjectを作る
Claudeで新しいProjectを作成し、名称を `SIMS Writer User Test RC1` とします。

## 2. Project Instructionsを設定する
`CLAUDE_PROJECT_INSTRUCTIONS.md`を開き、全文をProject Instructionsへ貼り付けて保存します。

## 3. Knowledgeを登録する
`knowledge/SIMS_WRITER_KNOWLEDGE_PACK.md`をProject Knowledgeへアップロードします。

## 4. 最初の動作確認
`examples/EXAMPLE_REQUEST.json`の内容を新しいチャットへ貼り付けます。ClaudeがJSON形式で応答し、本文不足時に推測せず確認を求めることを確認します。

## 5. 実記事テスト
`templates/IMPROVEMENT_REQUEST_TEMPLATE.json`を複製し、実記事の値を入力してClaudeへ送ります。1記事ごとに新しいチャットを推奨します。

## 6. 結果保存
Claudeの最終JSONを記事ごとに保存し、`REAL_ARTICLE_UAT_RESULT_TEMPLATE.json`へ評価を記録します。

## 禁止事項
- Repository ZIP全体をClaude Knowledgeへ入れない
- InstructionsファイルをKnowledgeへ入れない
- 本文がない状態で完成記事を要求しない
- Claudeの回答を確認せず公開しない
