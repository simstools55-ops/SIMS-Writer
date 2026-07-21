from __future__ import annotations
import json
from typing import Any

MAX_SOURCE_CHARS = 30000

def build_context_bundle(request: dict[str, Any], plan: dict[str, Any], **context: Any) -> dict[str, Any]:
    source = context.get("source_snapshot") or {}
    content = source.get("article_content") or source.get("raw_content")
    if isinstance(content, str) and len(content) > MAX_SOURCE_CHARS:
        content = content[:MAX_SOURCE_CHARS]
    return {
        "request": request,
        "content_plan": plan,
        "decision_action_plan": context.get("decision_action_plan", {}),
        "knowledge": context.get("knowledge_assembly", {}),
        "patterns": context.get("pattern_selection", {}),
        "source": {**source, "article_content": content},
        "quality_requirements": context.get("quality_requirements", []),
        "editorial_signals": context.get("editorial_signals") or (context.get("knowledge_assembly", {}) or {}).get("shared_editorial_signals", {}),
    }

def render_user_message(bundle: dict[str, Any]) -> str:
    return "次の構造化データに基づき、指定Schemaどおりの日本語記事成果物をJSONだけで返してください。\n" + json.dumps(bundle, ensure_ascii=False, indent=2)
