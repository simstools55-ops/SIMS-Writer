# ADR-0012 Provider-Neutral Model Adapter

## Status
Accepted

## Decision
Runtime Coreと外部LLMの間に、Provider非依存のModel Adapter ContractとTransport Protocolを置く。

## Rationale
ClaudeやOpenAI固有のRequest形式、応答形式、利用量情報をProduct Coreへ流入させず、Output ContractとQuality Gateを共通化するため。

## Consequences
ライブ接続にはProvider別Transport実装が必要だが、Context Builder、Output Parser、Validator、Fixture Testを共有できる。
