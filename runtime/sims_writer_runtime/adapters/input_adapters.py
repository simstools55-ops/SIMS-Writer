from __future__ import annotations

from typing import Any

from ..article_context import ArticleContextBuilder
from ..intake.request_loader import ImprovementRequestLoader


def normalize_generic(payload: dict[str, Any]) -> dict[str, Any]:
    """Compatibility adapter for existing callers.

    RuntimeOrchestrator now performs schema validation through
    ImprovementRequestLoader before this function is used.
    """
    if "payload" in payload and isinstance(payload["payload"], dict):
        payload = payload["payload"]
    request_id = payload.get("request_id") or "REQ-RUNTIME-DEMO"
    main_query = payload.get("main_query") or payload.get("query", {}).get("main_query")
    if not main_query:
        raise ValueError("main_query is required")
    return {
        "schema_version": str(payload.get("schema_version") or "1.0"),
        "request_id": request_id,
        "article_id": payload.get("article_id") or payload.get("article", {}).get("article_id"),
        "request_type": payload.get("request_type", "existing_article_improvement"),
        "language": payload.get("language", "ja-JP"),
        "main_query": main_query,
        "target_url": payload.get("target_url") or payload.get("article", {}).get("target_url"),
        "improvement_goal": payload.get("improvement_goal", []),
        "requested_output": payload.get("requested_output", ["publication_package"]),
        "source_system": payload.get("source_system") or "generic_json",
        "existing_content": payload.get("existing_content") or payload.get("article_content") or "",
        "current_title": payload.get("current_title") or payload.get("title") or "",
        "seo_title": payload.get("seo_title") or "",
        "meta_description": payload.get("meta_description") or "",
        "supporting_queries": payload.get("supporting_queries") or [],
        "performance": payload.get("performance") or {},
    }


def normalize_sbm(payload: dict[str, Any]) -> dict[str, Any]:
    main_query = payload.get("MainQuery") or payload.get("main_query")
    if not main_query:
        raise ValueError("MainQuery is required")
    return {
        "schema_version": str(payload.get("SchemaVersion") or "1.0"),
        "request_id": payload.get("RequestID", "REQ-SBM-DEMO"),
        "article_id": payload.get("ArticleID"),
        "request_type": "existing_article_improvement",
        "language": payload.get("Language") or "ja-JP",
        "main_query": main_query,
        "target_url": payload.get("URL"),
        "improvement_goal": payload.get("ImprovementGoal", []),
        "requested_output": payload.get("RequestedOutput") or ["publication_package", "before_after"],
        "source_system": "sims_blog_manager",
        "existing_content": payload.get("ExistingContent") or payload.get("ArticleContent") or "",
        "current_title": payload.get("ArticleTitle") or "",
        "seo_title": payload.get("SEOTitle") or "",
        "meta_description": payload.get("MetaDescription") or "",
        "supporting_queries": payload.get("SupportingQueries") or [],
        "performance": {
            "clicks": payload.get("Clicks"),
            "impressions": payload.get("Impressions"),
            "ctr": payload.get("CTR"),
            "average_position": payload.get("AveragePosition"),
        },
    }


def build_article_context(repo_root, payload: dict[str, Any], input_type: str = "auto") -> dict[str, Any]:
    loaded = ImprovementRequestLoader(repo_root).load(payload, input_type=input_type)
    return ArticleContextBuilder.build(loaded.payload).to_dict()
