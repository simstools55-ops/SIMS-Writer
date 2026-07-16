from __future__ import annotations
import json, re
from typing import Any

REQUIRED = ["seo_title", "meta_description", "h1", "article_content", "unresolved_items"]

def extract_json(text: str) -> dict[str, Any]:
    text=text.strip()
    if text.startswith("```"):
        text=re.sub(r"^```(?:json)?\s*", "", text)
        text=re.sub(r"\s*```$", "", text)
    try:
        value=json.loads(text)
    except json.JSONDecodeError:
        start=text.find("{"); end=text.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("Model output does not contain a JSON object")
        value=json.loads(text[start:end+1])
    if not isinstance(value, dict):
        raise ValueError("Model output root must be an object")
    return value

def validate_draft(value: dict[str, Any]) -> list[str]:
    errors=[]
    for key in REQUIRED:
        if key not in value: errors.append(f"missing:{key}")
    if value.get("article_content") is not None and not isinstance(value.get("article_content"), str):
        errors.append("type:article_content")
    if not isinstance(value.get("unresolved_items", []), list): errors.append("type:unresolved_items")
    return errors
