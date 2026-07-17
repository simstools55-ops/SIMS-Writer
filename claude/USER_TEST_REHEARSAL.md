# Claude Project 操作リハーサル

Version: 1.10.0-preview.1
Status: Developer Rehearsal

> この手順は開発者による事前確認用です。一般利用者テスト開始版ではありません。

## 目的

Claudeへ登録する配布ファイルだけで、改善依頼の投入から結果確認までの操作が再現できるかを確認します。

## 使用する配布ファイル

1. `CLAUDE_PROJECT_INSTRUCTIONS.md` — Project Instructionsへ全文を設定
2. `knowledge/SIMS_WRITER_KNOWLEDGE_PACK.md` — Project Knowledgeへ追加
3. `examples/EXAMPLE_REQUEST.json` — 正常系入力
4. `templates/IMPROVEMENT_REQUEST_TEMPLATE.json` — 新規依頼のひな形

## リハーサル手順

1. 新規Claude Projectを作成する。
2. Project Instructionsを設定する。
3. Knowledge Packを追加する。
4. `EXAMPLE_REQUEST.json`の内容をそのまま送信する。
5. 応答がJSONだけであることを確認する。
6. `status`が`generated`または`manual_review_required`であることを確認する。
7. `generated`の場合、完成記事・改善理由・FAQ・内部リンク候補を確認する。
8. 本文を空にした依頼を送信し、`manual_review_required`になることを確認する。
9. 記事カタログにないURLを内部リンクとして出していないことを確認する。
10. `TEST_CHECKLIST.md`へ結果を記録する。

## 中止条件

次のいずれかが発生した場合は、利用者テストへ進みません。

- JSON以外の長い前置きや後書きが付く
- 入力本文がないのに完成記事を生成する
- 入力に存在しないURLを内部リンク候補として生成する
- 不明な事実を断定する
- 必須キーが欠落する

## 判定

全項目に合格しても、実在記事による日本語品質UATと初心者環境での再現確認が終わるまでは一般利用者テストを開始しません。

## 実記事UAT結果の記録

各記事の確認後、`REAL_ARTICLE_UAT_RESULT_TEMPLATE.json`を複製し、6項目を1〜5点で評価してください。推測で合格にせず、未解決の問題は`blockers`へ記録します。
