from typing import Any

class ManualModelAdapter:
    name = "manual-structure-adapter"

    def produce(self, request: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
        # Alpha runtime intentionally does not claim article generation quality.
        return {
            "draft_status": "manual_review_required",
            "seo_title": None,
            "meta_description": None,
            "h1": None,
            "article_content": None,
            "unresolved_items": [
                "Production model adapter is not installed in v0.7.0-alpha.1",
                "Article content must be generated in the next adapter package",
            ],
            "plan_reference": plan.get("plan_id"),
        }
