# Migration Guide v0.2.0 Final

1. 既存SIMS-WriterへCore版を上書きする。
2. Claude Projectの旧SIMS Writer Knowledgeを削除する。
3. Final Claude版のProject Instructionsを設定する。
4. `runtime/ knowledge/ validation/ presentation/ contracts/ schemas/ templates/ examples/`を登録する。
5. テスト依頼1件でV2 JSONが出力されることを確認する。

V1 Schemaは削除必須ではないが、新規出力には使用しない。
