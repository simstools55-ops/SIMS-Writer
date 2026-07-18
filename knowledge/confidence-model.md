# Confidence Model v1.0

## 配点
| 要素 | 配点 |
|---|---:|
| Contract完全性 | 20 |
| Search Consoleデータ量 | 20 |
| 診断一貫性 | 15 |
| 本文取得完全性 | 15 |
| 監査間整合性 | 15 |
| Evidence確認可能性 | 10 |
| 改善履歴情報 | 5 |

## スコア帯
- 85〜100: HIGH
- 65〜84: MEDIUM
- 0〜64: LOW

## 強制LOW候補
- 本文大幅欠落
- main_query不明
- Search Diagnosis不能
- 監査結果が複数矛盾
- 対象期間不明
- 主要データが推定のみ

LOW_SAMPLEはConfidenceを1段階下げる。
