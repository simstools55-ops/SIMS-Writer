# Learning Registry Application v2.2

## Runtime rule

実記事テスト回答を評価するときは、記事修正案を作る前にLearning分類を確定します。

1. ARTICLE_SPECIFIC
2. PATTERN_CANDIDATE
3. MAPPING_DEFECT
4. VALIDATION_DEFECT
5. PREFERENCE_ONLY

## Product-change decision

- ARTICLE_SPECIFIC: 記事のみ
- PATTERN_CANDIDATE: Shared審査後に採用
- MAPPING_DEFECT: Snapshot/Runtime修正
- VALIDATION_DEFECT: Final QAと回帰修正
- PREFERENCE_ONLY: 変更なし

## Learning Sprint

10記事単位で分類別件数と未処理Learningを集計します。重大な安全性・Contract違反は即時処理します。
