from __future__ import annotations

from typing import Any

from ..vertical_slices.ctr_improvement import CTRImprovementSlice


class DeterministicImprovementAdapter:
    """Grounded alpha adapter for the first product vertical slice.

    It does not invent research or external evidence. It only transforms the
    validated request and supplied article source into a conservative CTR
    improvement proposal.
    """

    name = "deterministic-ctr-improvement-adapter"

    def __init__(self) -> None:
        self.slice = CTRImprovementSlice()

    def produce(self, request: dict[str, Any], plan: dict[str, Any], **kwargs: Any) -> dict[str, Any]:
        source_snapshot = kwargs.get("source_snapshot") or {}
        canonical = self._to_slice_request(request, source_snapshot)
        decision = self.slice.decide(canonical)
        draft = self.slice.build_draft(canonical, decision)
        draft["draft_status"] = "generated"
        draft["plan_reference"] = plan.get("plan_id")
        draft["adapter"] = self.name
        draft["before_after"] = {
            "seo_title": {
                "before": canonical.get("seo_title") or canonical.get("current_title") or "",
                "after": draft.get("seo_title") or "",
            },
            "introduction": {
                "before": self._existing_intro(source_snapshot),
                "after": draft.get("introduction") or "",
            },
        }
        draft["change_reasons"] = [x for x in decision.reason.split("。") if x]
        return draft

    @staticmethod
    def _existing_intro(source_snapshot: dict[str, Any]) -> str:
        text = (source_snapshot.get("normalized_text") or "").strip()
        if not text:
            return ""
        return text[:240]

    @staticmethod
    def _to_slice_request(request: dict[str, Any], source_snapshot: dict[str, Any]) -> dict[str, Any]:
        performance = request.get("performance") or {}
        existing = source_snapshot.get("normalized_text") or request.get("existing_content") or ""
        return {
            "request_id": request.get("request_id"),
            "article_id": request.get("article_id"),
            "target_url": request.get("target_url"),
            "current_title": request.get("current_title") or "",
            "seo_title": request.get("seo_title") or "",
            "meta_description": request.get("meta_description") or "",
            "main_query": request.get("main_query") or "",
            "supporting_queries": list(request.get("supporting_queries") or []),
            "existing_content": existing,
            "clicks": performance.get("clicks"),
            "impressions": performance.get("impressions"),
            "ctr": performance.get("ctr"),
            "average_position": performance.get("average_position"),
            "priority_components": list(request.get("improvement_goal") or []),
            "site_name": request.get("site_name") or "",
        }
