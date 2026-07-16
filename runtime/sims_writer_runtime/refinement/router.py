from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class RefinementRoute:
    issue_id: str
    rule_id: str
    target_component: str
    recovery_type: str
    return_stage: str
    automatic: bool

class IssueRouter:
    """Quality Issueを最小の修正単位と戻り先へ振り分ける。"""
    AUTO_RULES = {
        "QF-PUB-001": ("article", "placeholder_elimination"),
        "QF-JPN-003": ("article", "ai_phrase_reduction"),
        "QF-REA-003": ("article", "redundancy_reduction"),
        "QF-STR-001": ("sections", "heading_hierarchy_repair"),
    }
    STAGE_BY_RULE = {
        "QF-INT-001": "content_planning", "QF-INT-002": "content_planning",
        "QF-INT-003": "content_planning", "QF-FAC-001": "source_acquisition",
        "QF-FAC-002": "source_acquisition", "QF-SAF-001": "manual_review",
        "QF-SAF-002": "manual_review", "QF-SAF-003": "content_production",
        "QF-SEO-001": "content_production", "QF-PUB-002": "content_production",
        "QF-PUB-003": "content_production", "QF-PUB-004": "content_production",
    }

    def route(self, issue: dict[str, Any]) -> RefinementRoute:
        rid = issue.get("rule_id", "UNKNOWN")
        component = issue.get("component") or "article"
        if rid in self.AUTO_RULES:
            component, recovery = self.AUTO_RULES[rid]
            return RefinementRoute(issue.get("issue_id", rid), rid, component, recovery, "refinement", True)
        stage = self.STAGE_BY_RULE.get(rid, "content_production")
        recovery = "manual_review" if stage == "manual_review" else "targeted_model_revision"
        return RefinementRoute(issue.get("issue_id", rid), rid, component, recovery, stage, False)
