from __future__ import annotations
from typing import Any

SEO_CRITICAL_RULES = {
    "QF-INT-001", "QF-INT-002", "QF-SEO-001", "QF-SAF-001", "QF-SAF-002",
    "QF-SAF-003", "QF-FAC-005", "QF-PUB-002", "QF-PUB-005", "QF-PUB-006",
    "QF-COM-004", "QF-ORG-003", "QF-EEA-003",
}


REVENUE_CRITICAL_RULES = {
    "QF-CTR-001", "QF-WQP-001", "QF-DRIFT-001", "QF-CAN-001", "QF-LINK-001",
}

def revenue_tier(issue: dict[str, Any]) -> str:
    """Classify findings by material impact, not editorial perfection."""
    severity = str(issue.get("severity") or "").lower()
    rule_id = str(issue.get("rule_id") or "")
    material = bool(issue.get("material_seo_impact") or issue.get("material_reader_risk"))
    if severity in {"blocker", "critical"} or rule_id in SEO_CRITICAL_RULES or rule_id in REVENUE_CRITICAL_RULES or material:
        return "revenue_or_safety_critical"
    if issue.get("auto_repairable") or severity in {"major", "error"}:
        return "auto_repair"
    return "non_blocking_quality"

def classify_issue(issue: dict[str, Any]) -> str:
    severity = str(issue.get("severity") or "").lower()
    rule_id = str(issue.get("rule_id") or "")
    if severity in {"blocker", "critical"} or rule_id in SEO_CRITICAL_RULES:
        return "seo_critical"
    return "quality_recommendation"


def split_issues(issues: list[dict[str, Any]] | None) -> dict[str, list[dict[str, Any]]]:
    result = {
        "seo_critical": [], "quality_recommendation": [],
        "revenue_or_safety_critical": [], "auto_repair": [], "non_blocking_quality": [],
    }
    for issue in issues or []:
        result[classify_issue(issue)].append(issue)
        result[revenue_tier(issue)].append(issue)
    return result
