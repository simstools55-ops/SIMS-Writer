# Before / After Template v2.1

各変更は次の順序を崩さない。

1. Before
2. After
3. 期待する効果
4. 変更理由

## 表示ルール

- 短文は独立した `text` コードブロックにする。
- 長文は `max-height:24rem; overflow-y:auto` の枠内で縦スクロール表示する。
- 横スクロールは原則使用せず、`white-space:pre-wrap` と `overflow-wrap:anywhere` で折り返す。
- BeforeとAfterは別々の枠にする。
- Afterは省略せず、そのまま記事へ貼り付けられる完成形にする。
- 複数見出しをまとめて曖昧に変更せず、一対一で対応させる。
- 変更しない項目は出力しない。

長文用HTMLは `PRESENTATION_TEMPLATE.md` の定型を使用する。表示環境がHTML styleを無効化する場合だけコードブロックへフォールバックする。
