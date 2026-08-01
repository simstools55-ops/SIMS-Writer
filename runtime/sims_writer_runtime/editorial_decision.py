from __future__ import annotations

from copy import deepcopy
from typing import Any

from .evidence_layer import evidence_level, enforce_evidence_boundaries, LOW, NONE
from .progressive_editing import apply_progressive_editing
from .editorial_strategy import attach_strategy

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
    when it is complete, supported and free from unresolved human decisions. Low-evidence drafts are repaired or rejected internally; they are not delegated to the user unless a genuine owner signal is present.
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
    level = evidence_level(change)
    if level == NONE or change.get("evidence_sufficient") is False:
        return INTERNAL_REJECT
    if level == LOW:
        return INTERNAL_REJECT
    if change.get("copy_ready") is False:
        return INTERNAL_REJECT
    return PUBLIC_OK


def build_publication_result(changes: list[dict[str, Any]], *, serp_status: str | None = None, strategy: dict[str, Any] | None = None) -> dict[str, Any]:
    public_ok: list[dict[str, Any]] = []
    user_decision: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    if strategy:
        changes = attach_strategy(changes, strategy)
    changes, evidence_findings = enforce_evidence_boundaries(changes)
    progressive_trace: list[dict[str, Any]] = []
    if serp_status is not None:
        changes, progressive_trace = apply_progressive_editing(changes, serp_status=serp_status)

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
        "_internal_evidence_findings": evidence_findings,
        "_internal_progressive_trace": progressive_trace,
        "_internal_editorial_strategy": deepcopy(strategy or {}),
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
            "evidence_findings": deepcopy(publication_result.get("_internal_evidence_findings") or []),
            "progressive_trace": deepcopy(publication_result.get("_internal_progressive_trace") or []),
            "editorial_strategy": deepcopy(publication_result.get("_internal_editorial_strategy") or {}),
        },
    }


def user_visible_publication_result(publication_result: dict[str, Any]) -> dict[str, Any]:
    """Remove every internal-only field before user/SBM serialization."""
    public_ok = deepcopy(publication_result.get("public_ok_changes") or [])
    user_decision = deepcopy(publication_result.get("user_decision_changes") or [])
    return {
        "publishable_public_ok_changes": bool(public_ok),
        "has_user_decision_changes": bool(user_decision),
        "change_summary": deepcopy(publication_result.get("change_summary") or []),
        "public_ok_changes": public_ok,
        "user_decision_changes": user_decision,
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
        "decision_trace": deepcopy(item.get("decision_trace") or [
            "公開に必要な確認事項を検出",
            "確認完了まで利用者判断として保留",
        ]),
    }
