from __future__ import annotations
import json
from typing import Any, Callable
from .model_protocol import ModelRequest, ModelResponse

class CallableTransport:
    def __init__(self, provider: str, caller: Callable[[dict[str, Any]], dict[str, Any]], response_parser: Callable[[dict[str, Any]], ModelResponse]):
        self.provider=provider; self._caller=caller; self._parser=response_parser
    def invoke(self, request: ModelRequest) -> ModelResponse:
        return self._parser(self.build_payload(request)) if False else self._parser(self._caller(self.build_payload(request)))
    def build_payload(self, request: ModelRequest) -> dict[str, Any]:
        raise NotImplementedError

class ClaudeMessagesTransport(CallableTransport):
    def __init__(self, caller): super().__init__("claude", caller, self.parse_response)
    def build_payload(self, request: ModelRequest) -> dict[str, Any]:
        return {"model":request.model,"system":request.system,"messages":request.messages,"temperature":request.temperature,"max_tokens":16000}
    @staticmethod
    def parse_response(raw: dict[str, Any]) -> ModelResponse:
        blocks=raw.get("content",[]); text="".join(x.get("text","") for x in blocks if isinstance(x,dict))
        return ModelResponse(text=text,model=raw.get("model","unknown"),provider="claude",usage=raw.get("usage",{}),raw=raw)

class OpenAIResponsesTransport(CallableTransport):
    def __init__(self, caller): super().__init__("openai", caller, self.parse_response)
    def build_payload(self, request: ModelRequest) -> dict[str, Any]:
        return {"model":request.model,"instructions":request.system,"input":request.messages,"temperature":request.temperature,"text":{"format":{"type":"json_schema","name":"content_draft","schema":request.output_schema,"strict":True}}}
    @staticmethod
    def parse_response(raw: dict[str, Any]) -> ModelResponse:
        text=raw.get("output_text","")
        if not text:
            parts=[]
            for item in raw.get("output",[]):
                for c in item.get("content",[]) if isinstance(item,dict) else []:
                    if c.get("type") in ("output_text","text"): parts.append(c.get("text",""))
            text="".join(parts)
        return ModelResponse(text=text,model=raw.get("model","unknown"),provider="openai",usage=raw.get("usage",{}),raw=raw)

class GenericChatTransport(CallableTransport):
    def __init__(self, caller): super().__init__("generic", caller, self.parse_response)
    def build_payload(self, request: ModelRequest) -> dict[str, Any]:
        return {"model":request.model,"messages":[{"role":"system","content":request.system},*request.messages],"response_schema":request.output_schema,"temperature":request.temperature}
    @staticmethod
    def parse_response(raw: dict[str, Any]) -> ModelResponse:
        text=raw.get("text") or raw.get("content") or ""
        return ModelResponse(text=text,model=raw.get("model","unknown"),provider="generic",usage=raw.get("usage",{}),raw=raw)
