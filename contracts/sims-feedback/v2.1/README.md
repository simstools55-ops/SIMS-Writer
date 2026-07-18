# SIMS Feedback JSON Contract v2.1

本文出力と同一のRuntime Stateから生成する機械処理用契約です。`decision`が変更範囲を支配し、重大な前提誤りは`stop_and_rewrite`になります。

## v1互換

v1.x入力は受理し、既存フィールドを`legacy`へ保持しながらv2.1へ正規化します。推定・警告・理由を混同せず、未知フィールドは黙って破棄しません。
