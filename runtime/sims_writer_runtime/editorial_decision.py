from __future__ import annotations

from copy import deepcopy
from typing import Any

PUBLIC_OK = "PUBLIC_OK"
USER_DECISION = "USER_DECISION"
INTERNAL_REJECT = "INTERNAL_REJECT"
VISIBLE_DECISIONS = {PUBLIC_OK, USER_DECISION}

_USER_DECISION_SIGNALS = {
    "author_experience", "brand_policy", "freshness_confirmation",
    "commercial_claim", "medical_legal_financial_claim", "strategic_tradeoff",
    "link_destination_confirmation", "first_party_fact_confirmation",
}


def classify_change(change: dict[str, Any]) -> str:
    """Classify one proposed edit after internal QA.

    The classifier is intentionally conservative. A change is PUBLIC_OK only
    when it is complete, supported and free from unresolved human decisions.
    """
    if change.get("rejected") or change.get("internal_reject"):
        return INTERNAL_REJECT
    if change.get("qa_status") in {"FAIL", "REQUIRED_FIX", "UNVERIFIABLE"}:
        return INTERNAL_REJECT
    if not str(change.get("after") or "").strip():
        return INTERNAL_REJECT
    if change.get("before") == change.get("after"):
        return INTERNAL_REJECT
    signals = set(change.get("decision_signals") or [])
    if change.get("requires_user_confirmation") or signals & _USER_DECISION_SIGNALS:
        return USER_DECISION
    if change.get("evidence_sufficient") is False:
        return INTERNAL_REJECT
    if change.get("copy_ready") is False:
        return INTERNAL_REJECT
    return PUBLIC_OK


def build_publication_result(changes: list[dict[str, Any]]) -> dict[str, Any]:
    public_ok: list[dict[str, Any]] = []
    user_decision: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for raw in changes:
        item = deepcopy(raw)
        decision = item.get("editorial_decision") or classify_change(item)
        item["editorial_decision"] = decision
        if decision == PUBLIC_OK:
            public_ok.append(_public_item(item))
        elif decision == USER_DECISION:
            user_decision.append(_decision_item(item))
        else:
            rejected.append(item)

    visible = public_ok + user_decision
    return {
        "change_summary": [item.get("component_label") or item.get("component") for item in visible],
        "public_ok_changes": public_ok,
        "user_decision_changes": user_decision,
        "_internal_rejected_changes": rejected,
    }


def build_internal_audit_record(*, publication_result: dict[str, Any], qa_result: dict[str, Any],
                                analysis: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build the non-user-facing audit record."""
    return {
        "record_type": "SIMS_WRITER_INTERNAL_AUDIT_V1",
        "analysis": deepcopy(analysis or {}),
        "qa": deepcopy(qa_result),
        "editorial_decisions": {
            "public_ok_count": len(publication_result.get("public_ok_changes") or []),
            "user_decision_count": len(publication_result.get("user_decision_changes") or []),
            "internal_reject_count": len(publication_result.get("_internal_rejected_changes") or []),
            "internal_rejected_changes": deepcopy(publication_result.get("_internal_rejected_changes") or []),
        },
    }


def user_visible_publication_result(publication_result: dict[str, Any]) -> dict[str, Any]:
    """Remove every internal-only field before user/SBM serialization."""
    return {
        "change_summary": deepcopy(publication_result.get("change_summary") or []),
        "public_ok_changes": deepcopy(publication_result.get("public_ok_changes") or []),
        "user_decision_changes": deepcopy(publication_result.get("user_decision_changes") or []),
    }


def _public_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "component": item.get("component"),
        "component_label": item.get("component_label") or item.get("label") or item.get("component"),
        "before": item.get("before"),
        "after": item.get("after"),
        "implementation_instruction": item.get("implementation_instruction") or "現在の内容と置き換えてください。",
    }


def _decision_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "component": item.get("component"),
        "component_label": item.get("component_label") or item.get("label") or item.get("component"),
        "before": item.get("before"),
        "after": item.get("after"),
        "decision_reason": item.get("decision_reason") or "利用者による事実または運営方針の確認が必要です。",
        "benefit_if_adopted": item.get("benefit_if_adopted") or "確認後に採用することで、改善意図を安全に反映できます。",
        "impact_if_not_adopted": item.get("impact_if_not_adopted") or "採用しなくても現在の内容は維持されます。",
        "confirmation_point": item.get("confirmation_point") or "修正内容が実際の事実・体験・運営方針に合うか確認してください。",
    }
