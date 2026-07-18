# Gate Decision Matrix v1.0

| Blocking | Conflict | Confidence | Risk | Warning | Decision |
|---|---|---|---|---|---|
| Yes | Any | Any | Any | Any | BLOCK |
| No | Critical | Any | Any | Any | REVIEW_REQUIRED |
| No | None | LOW | HIGH | Any | REVIEW_REQUIRED |
| No | None | LOW | LOW/MEDIUM | Yes | PASS_WITH_WARNING |
| No | None | MEDIUM/HIGH | HIGH | Yes | PASS_WITH_WARNING または REVIEW_REQUIRED |
| No | None | MEDIUM/HIGH | LOW/MEDIUM | Yes | PASS_WITH_WARNING |
| No | None | MEDIUM/HIGH | LOW/MEDIUM | No | PASS |

## 常時BLOCK
- ArticleID不一致
- URL不一致
- 必須外部形式破損
- 対象記事特定不能
- Before/After対応不能

## Evidence
- E3未確認の重大中心主張: BLOCK
- E2未確認の中心主張: REVIEWまたはWarning
- 軽微な出典不足: Warning

## Strategy
- no_change + 大量変更: REVIEW
- L5/S5 + Preservation 75以上: REVIEW
- L4/L5 + LOW_SAMPLE: REVIEW
- Budget超過20ポイント未満: Warning
- Budget超過20ポイント以上: REVIEW
