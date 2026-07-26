from __future__ import annotations

from copy import deepcopy
from typing import Any

HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"
NONE = "NONE"


def evidence_level(record: dict[str, Any]) -> str:
    """Return a conservative evidence level for one material claim."""
    has_evidence_metadata = any(k in record for k in ("evidence_level", "primary_evidence", "secondary_evidence", "article_evidence", "freshness_status", "contradicted"))
    if not has_evidence_metadata:
        return MEDIUM
    explicit = str(record.get("evidence_level") or "").upper()
    if explicit in {HIGH, MEDIUM, LOW, NONE}:
        return explicit
    if record.get("contradicted"):
        return NONE
    if record.get("primary_evidence") and record.get("freshness_status") in {"current", "not_applicable"}:
        return HIGH
    if record.get("article_evidence") and record.get("secondary_evidence"):
        return MEDIUM
    if record.get("secondary_evidence") or record.get("article_evidence"):
        return LOW
    return NONE


def classify_gap(gap: dict[str, Any]) -> str:
    """Combine query, verified SERP and evidence into one planning classification."""
    level = evidence_level(gap)
    relevant = bool(gap.get("query_signal") or gap.get("serp_signal"))
    if gap.get("separate_intent"):
        return "SEPARATE_INTENT"
    if not relevant:
        return "NO_GAP"
    if level in {HIGH, MEDIUM} and gap.get("serp_status") == "verified":
        return "SUPPORTED_GAP"
    if level == LOW:
        return "DECISION_GAP"
    return "UNSUPPORTED_GAP"


def enforce_evidence_boundaries(changes: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Prevent low/none evidence claims from leaking into PUBLIC_OK changes."""
    items = deepcopy(changes)
    restricted: dict[str, str] = {}
    for item in items:
        for claim in item.get("claims") or []:
            cid = str(claim.get("claim_id") or "").strip()
            level = evidence_level(claim)
            if cid and level in {LOW, NONE}:
                restricted[cid] = level

    findings: list[dict[str, Any]] = []
    for item in items:
        used = set(item.get("claim_ids") or [])
        contamination = sorted(cid for cid in used if cid in restricted)
        if not contamination:
            continue
        levels = {restricted[cid] for cid in contamination}
        previous = item.get("editorial_decision")
        if NONE in levels:
            item["editorial_decision"] = "INTERNAL_REJECT"
            item["qa_status"] = "UNVERIFIABLE"
        else:
            item["editorial_decision"] = "USER_DECISION"
            item["requires_user_confirmation"] = True
            item.setdefault("decision_reason", "公開文に未確認の事実が含まれるため、根拠確認が必要です。")
            item.setdefault("confirmation_point", "一次情報または信頼できる最新資料で該当事実を確認してください。")
        findings.append({
            "code": "EVIDENCE-CONTAMINATION-001",
            "component": item.get("component"),
            "claim_ids": contamination,
            "previous_decision": previous,
            "final_decision": item.get("editorial_decision"),
        })
    return items, findings
