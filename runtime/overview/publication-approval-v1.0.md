# Publication Approval Runtime v1.0

## Purpose

公開成果物をExecution ID単位で保留、承認、却下、確定する。

## States

`pending_review` → `approved` → `finalized`

`pending_review`または`approved`から`rejected`へ遷移できる。`finalized`は変更不可。

## Safety rules

- `artifact-validation.json`が`valid`かつ`release_ready=true`の場合だけ承認できる。
- 承認対象のExecution IDは現在の成果物と一致しなければならない。
- 却下にはReviewerと理由を必須とする。
- 確定には事前承認を必須とする。
- 確定時は`release/<execution_id>/`へ成果物をコピーし、SHA-256を記録する。

## Artifacts

- `publication-approval.json`
- `approval-history.json`
- `finalization-manifest.json`
- `release/<execution_id>/`
