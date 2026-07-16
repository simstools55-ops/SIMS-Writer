from __future__ import annotations
from typing import Any
from .model_protocol import ModelRequest, ModelTransport
from .context_builder import build_context_bundle, render_user_message
from .output_parser import extract_json, validate_draft

DRAFT_SCHEMA = {
  "type":"object",
  "required":["seo_title","meta_description","h1","article_content","unresolved_items"],
  "properties":{
    "seo_title":{"type":["string","null"]},
    "meta_description":{"type":["string","null"]},
    "h1":{"type":["string","null"]},
    "article_content":{"type":["string","null"]},
    "faq":{"type":"array"},
    "internal_link_recommendations":{"type":"array"},
    "unresolved_items":{"type":"array","items":{"type":"string"}}
  }
}

SYSTEM = """あなたはSIMS WriterのProduction Adapterです。Content Plan、Decision、Knowledge、Patternに従い、事実を創作せず、指定されたJSON Schemaだけを返してください。確認不能事項はunresolved_itemsへ記録してください。"""

class StructuredModelAdapter:
    name="structured-model-adapter"
    def __init__(self, transport: ModelTransport, model: str):
        self.transport=transport; self.model=model
    def produce(self, request: dict[str, Any], plan: dict[str, Any], **context: Any) -> dict[str, Any]:
        bundle=build_context_bundle(request, plan, **context)
        mr=ModelRequest(model=self.model, system=SYSTEM, messages=[{"role":"user","content":render_user_message(bundle)}], output_schema=DRAFT_SCHEMA)
        response=self.transport.invoke(mr)
        draft=extract_json(response.text)
        errors=validate_draft(draft)
        if errors: raise ValueError("Invalid model draft: "+", ".join(errors))
        draft["draft_status"] = "generated" if draft.get("article_content") else "manual_review_required"
        draft["plan_reference"] = plan.get("plan_id")
        draft["generation_record"] = {"provider":response.provider,"model":response.model,"usage":response.usage}
        return draft
