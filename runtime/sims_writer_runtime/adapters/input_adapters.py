from typing import Any
import re


def _infer_main_query(payload: dict[str, Any]) -> tuple[str, bool]:
    """Return a usable query when possible without stopping the pipeline."""
    direct = payload.get("main_query") or payload.get("MainQuery") or payload.get("query", {}).get("main_query")
    if direct and str(direct).strip():
        return str(direct).strip(), False
    title = (payload.get("seo_title") or payload.get("SEOTitle") or payload.get("current_title")
             or payload.get("ArticleTitle") or payload.get("title") or "")
    clean = re.sub(r"[｜|].*$", "", str(title))
    clean = re.sub(r"【[^】]*】", "", clean)
    clean = re.sub(r"を(?:5つ|５つ|\d+つ)の項目で比較.*$", " 比較", clean)
    clean = re.sub(r"[！!？?]+$", "", clean).strip()
    return re.sub(r"\s+", " ", clean)[:120], bool(clean)


def normalize_generic(payload: dict[str, Any]) -> dict[str, Any]:
    if "payload" in payload and isinstance(payload["payload"], dict):
        payload = payload["payload"]
    request_id = payload.get("request_id") or "REQ-RUNTIME-DEMO"
    main_query, inferred = _infer_main_query(payload)
    return {
        "request_id": request_id,
        "request_type": payload.get("request_type", "existing_article_improvement"),
        "language": payload.get("language", "ja-JP"),
        "main_query": main_query,
        "main_query_inferred": inferred,
        "main_query_missing": not bool(main_query),
        "target_url": payload.get("article_url") or payload.get("ArticleURL") or payload.get("target_url") or payload.get("article", {}).get("target_url"),
        "site_id": payload.get("site_id") or payload.get("SiteID") or payload.get("site", {}).get("site_id"),
        "site_name": payload.get("site_name") or payload.get("SiteName") or payload.get("site", {}).get("site_name"),
        "site_url": payload.get("site_url") or payload.get("SiteURL") or payload.get("site", {}).get("site_url"),
        "article_id": payload.get("article_id") or payload.get("ArticleID"),
        "improvement_goal": payload.get("improvement_goal", []),
        "requested_output": payload.get("requested_output", ["publication_package"]),
        "source": "generic_json",
        "existing_content": payload.get("existing_content") or payload.get("article_content") or "",
        "current_title": payload.get("current_title") or payload.get("title") or "",
        "seo_title": payload.get("seo_title") or "",
        "meta_description": payload.get("meta_description") or "",
        "supporting_queries": payload.get("supporting_queries") or [],
        "performance": payload.get("performance") or {},
        "article_catalog": payload.get("article_catalog") or payload.get("ArticleCatalog") or [],
        "source_evidence": payload.get("source_evidence") or payload.get("SourceEvidence") or [],
    }


def normalize_sbm(payload: dict[str, Any]) -> dict[str, Any]:
    main_query, inferred = _infer_main_query(payload)
    return {
        "request_id": payload.get("RequestID", "REQ-SBM-DEMO"),
        "request_type": "existing_article_improvement",
        "language": "ja-JP",
        "main_query": main_query,
        "main_query_inferred": inferred,
        "main_query_missing": not bool(main_query),
        "target_url": payload.get("ArticleURL") or payload.get("URL"),
        "site_id": payload.get("SiteID"),
        "site_name": payload.get("SiteName"),
        "site_url": payload.get("SiteURL"),
        "article_id": payload.get("ArticleID"),
        "improvement_goal": payload.get("ImprovementGoal", []),
        "requested_output": ["publication_package", "before_after"],
        "source": "sims_blog_manager",
        "existing_content": payload.get("ExistingContent") or payload.get("ArticleContent") or "",
        "current_title": payload.get("ArticleTitle") or "",
        "seo_title": payload.get("SEOTitle") or "",
        "meta_description": payload.get("MetaDescription") or "",
        "supporting_queries": payload.get("SupportingQueries") or [],
        "performance": {"clicks": payload.get("Clicks"), "impressions": payload.get("Impressions"), "ctr": payload.get("CTR"), "average_position": payload.get("AveragePosition")},
        "article_catalog": payload.get("ArticleCatalog") or payload.get("article_catalog") or [],
        "source_evidence": payload.get("SourceEvidence") or payload.get("source_evidence") or [],
    }
