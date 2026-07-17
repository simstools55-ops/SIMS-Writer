# ADR-0018: Human and Machine Output Separation

- Status: Accepted
- Date: 2026-07-17

## Context

実記事テスト8件で、利用者向け改善案とSIMS_FEEDBACK JSONが混在し、全文重複、JSON順序違反、変更フラグ不整合が発生した。

## Decision

利用者向け成果物と機械連携Feedbackを別レイヤーにする。既定モードは `partial` とし、記事全文は `full` または `publish` でのみ許可する。Feedbackは必ず最終要素とし、その後に文章を出力しない。

## Consequences

- 修正箇所をBefore/Afterで把握しやすくなる。
- JSONが安定して機械処理できる。
- Output Contract ValidatorをRelease Gateに追加する。
