# SIMS Writer Official Regression Suite v1

5記事の公開前QAを再現する固定回帰スイート。

## Current state
評価プロファイル、期待判定、許可Auto-Fix、禁止処置、Runnerは完成。元のSBM依頼文とWriter回答は未収録のため、Fixture実行は`SKIP`となる。

## Freeze policy
`input.md`と`original_output.md`を登録した後は書き換えない。期待値の変更は理由とバージョンを記録する。

## Run
`python tools/run_official_regression.py`
