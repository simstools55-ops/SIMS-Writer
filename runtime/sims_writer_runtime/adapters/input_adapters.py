from typing import Any

def normalize_generic(payload: dict[str, Any]) -> dict[str, Any]:
    if "payload" in payload and isinstance(payload["payload"], dict):
        payload = payload["payload"]
    request_id = payload.get("request_id") or "REQ-RUNTIME-DEMO"
    main_query = payload.get("main_query") or payload.get("query", {}).get("main_query")
    if not main_query:
        raise ValueError("main_query is required")
    return {
        "request_id": request_id,
        "request_type": payload.get("request_type", "existing_article_improvement"),
        "language": payload.get("language", "ja-JP"),
        "main_query": main_query,
        "target_url": payload.get("target_url") or payload.get("article", {}).get("target_url"),
        "improvement_goal": payload.get("improvement_goal", []),
        "requested_output": payload.get("requested_output", ["publication_package"]),
        "source": "generic_json",
    }

def normalize_sbm(payload: dict[str, Any]) -> dict[str, Any]:
    main_query = payload.get("MainQuery") or payload.get("main_query")
    if not main_query:
        raise ValueError("MainQuery is required")
    return {
        "request_id": payload.get("RequestID", "REQ-SBM-DEMO"),
        "request_type": "existing_article_improvement",
        "language": "ja-JP",
        "main_query": main_query,
        "target_url": payload.get("URL"),
        "improvement_goal": payload.get("ImprovementGoal", []),
        "requested_output": ["publication_package", "before_after"],
        "source": "sims_blog_manager",
    }
