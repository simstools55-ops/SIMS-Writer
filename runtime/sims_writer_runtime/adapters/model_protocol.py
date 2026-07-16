from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Protocol

@dataclass
class ModelRequest:
    model: str
    system: str
    messages: list[dict[str, str]]
    output_schema: dict[str, Any]
    temperature: float = 0.2
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ModelResponse:
    text: str
    model: str
    provider: str
    usage: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

class ModelTransport(Protocol):
    provider: str
    def invoke(self, request: ModelRequest) -> ModelResponse: ...

class ProductionAdapter(Protocol):
    name: str
    def produce(self, request: dict[str, Any], plan: dict[str, Any], **context: Any) -> dict[str, Any]: ...
