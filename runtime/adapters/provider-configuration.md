# Provider Configuration

外部API接続は実行環境側で設定する。RepositoryへAPIキーを保存しない。

- `SIMS_WRITER_PROVIDER`: `claude` / `openai` / `generic`
- `SIMS_WRITER_MODEL`: 利用するモデル識別子
- API Key: Provider公式SDKまたは接続層が環境変数から取得

AdapterはTransport Protocolへ依存し、SDKやHTTP実装は交換可能である。
