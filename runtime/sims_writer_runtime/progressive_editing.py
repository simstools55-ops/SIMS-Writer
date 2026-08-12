from __future__ import annotations

from copy import deepcopy
from typing import Any

from .knowledge_confidence import publication_ceiling

PUBLIC_OK = "PUBLIC_OK"
USER_DECISION = "USER_DECISION"
INTERNAL_REJECT = "INTERNAL_REJECT"

_PRESENTATION_COMPONENTS = {"seo_title", "meta_description", "introduction"}
_STRUCTURAL_COMPONENTS = {"headings", "faq", "body", "structure", "images"}
_MECHANICAL_BASES = {"mechanical", "accuracy", "consistency", "usability"}
_SERP_BASES = {"search_intent", "serp_gap", "secondary_query_expansion", "competitor_gap"}


def progressive_decision(change: dict[str, Any], *, serp_status: str) -> str:
    """Return the maximum safe editorial decision for one component.

    Progressive editing never treats the whole article as one gate. It combines
    SERP verification scope, claim evidence and the requested component.
    """
    item = deepcopy(change)
    component = str(item.get("component") or "").strip()
    basis = str(item.get("change_basis") or "").strip()
    evidence = str(item.get("evidence_level") or "MEDIUM").upper()
    current = str(item.get("editorial_decision") or "").upper()

    ceiling = publication_ceiling(item) if any(k in item for k in ("source_level","evidence_source_level","verified_at","last_verified_at","knowledge_confidence")) else None
    if ceiling == INTERNAL_REJECT:
        return INTERNAL_REJECT
    if ceiling == USER_DECISION and current != INTERNAL_REJECT:
        return INTERNAL_REJECT

    if current == INTERNAL_REJECT or item.get("internal_reject"):
        return INTERNAL_REJECT
    if evidence == "NONE":
        return INTERNAL_REJECT
    if evidence == "LOW":
        return INTERNAL_REJECT
    if item.get("requires_user_confirmation") and str(item.get("user_confirmation_kind") or "").lower() in {
        "experience", "first_party_fact", "rights", "permission", "contract", "sponsorship",
        "brand_policy", "irreversible_site_action", "owner_intent"
    }:
        return USER_DECISION

    status = str(serp_status or "unavailable").lower()
    if status == "verified":
        return PUBLIC_OK

    # Non-SERP mechanical and verified factual corrections may always progress.
    if basis in _MECHANICAL_BASES and not item.get("changes_search_promise"):
        return PUBLIC_OK

    if status == "partial":
        # Presentation-layer copy can progress when it only reflects the current
        # article and inspected evidence; it must not assert an unverified gap.
        if component in _PRESENTATION_COMPONENTS:
            if item.get("serp_gap_required") or item.get("introduces_new_claim"):
                return INTERNAL_REJECT
            return PUBLIC_OK
        # Structural/content expansion needs stronger coverage. With partial
        # SERP it may be shown for user confirmation only when evidence exists.
        if component in _STRUCTURAL_COMPONENTS:
            return INTERNAL_REJECT
        return INTERNAL_REJECT

    # unavailable: only the non-SERP whitelist above can progress.
    if basis in _SERP_BASES or component in _PRESENTATION_COMPONENTS | _STRUCTURAL_COMPONENTS:
        return INTERNAL_REJECT
    return INTERNAL_REJECT


def apply_progressive_editing(changes: list[dict[str, Any]], *, serp_status: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Apply component-scoped progressive decisions and return internal trace."""
    output=[]
    trace=[]
    for raw in changes:
        item=deepcopy(raw)
        previous=item.get("editorial_decision")
        decision=progressive_decision(item, serp_status=serp_status)
        item["editorial_decision"]=decision
        item["progressive_scope"]={
            "serp_status": str(serp_status or "unavailable").lower(),
            "component": item.get("component"),
            "evidence_level": str(item.get("evidence_level") or "MEDIUM").upper(),
        }
        output.append(item)
        trace.append({
            "component": item.get("component"),
            "previous_decision": previous,
            "final_decision": decision,
            "serp_status": str(serp_status or "unavailable").lower(),
        })
    return output, trace
