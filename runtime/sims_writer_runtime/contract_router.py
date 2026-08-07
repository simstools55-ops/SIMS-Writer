from __future__ import annotations

from copy import deepcopy
from typing import Any

TREATMENT_REQUEST_FORMAT = "SIMS_WRITER_TREATMENT_REQUEST_V1"
TREATMENT_RESULT_FORMAT = "SIMS_WRITER_TREATMENT_RESULT_V1"
LEGACY_FEEDBACK_FORMAT = "SIMS_FEEDBACK_V2"
DOCTOR_REFERRAL_MODE = "DOCTOR_REFERRAL_TREATMENT"


def expected_output_contract(request: dict[str, Any]) -> tuple[str, str]:
    """Resolve the machine result contract from the incoming SBM request.

    return_contract is authoritative. Doctor Referral Treatment must never fall back to
    SIMS_FEEDBACK_V2. Standard/legacy requests retain SIMS_FEEDBACK_V2 compatibility.
    """
    return_contract = request.get("return_contract") or {}
    fmt = str(return_contract.get("format") or "").strip()
    ver = str(return_contract.get("contract_version") or "").strip()
    if fmt:
        return fmt, ver or ("1.0" if fmt == TREATMENT_RESULT_FORMAT else "4.2")
    if request.get("format") == TREATMENT_REQUEST_FORMAT or request.get("request_mode") == DOCTOR_REFERRAL_MODE:
        return TREATMENT_RESULT_FORMAT, "1.0"
    return LEGACY_FEEDBACK_FORMAT, "4.2"


def build_treatment_result_v1(*, request: dict[str, Any], publication_result: dict[str, Any],
                              performed_changes: list[dict[str, Any]] | None = None,
                              treatment_status: str = "COMPLETED",
                              completed_at: str = "", recommended_review_days: int | None = None,
                              next_action: str = "monitor") -> dict[str, Any]:
    """Build the compact SBM-facing treatment result shape accepted by SBM.

    The Human Layer remains unchanged; this function only selects/builds the final machine JSON.
    """
    case_id = str(request.get("case_id") or "")
    article = request.get("article") or {}
    doctor = request.get("doctor_referral") or {}
    allowed = list(doctor.get("allowed_scope") or [])
    blocked = list(doctor.get("blocked_scope") or [])
    changes = deepcopy(performed_changes if performed_changes is not None else (publication_result.get("public_ok_changes") or []))
    result = {
        "format": TREATMENT_RESULT_FORMAT,
        "contract_version": "1.0",
        "case_id": case_id,
        "article_id": str(request.get("article_id") or article.get("article_id") or ""),
        "site_id": str(request.get("site_id") or ""),
        "completed_at": completed_at,
        "treatment_status": treatment_status,
        "referral_compliance": {
            "compliant": True,
            "performed_scope": allowed,
            "blocked_scope_touched": [],
            "scope_violations": [],
        },
        "performed_changes": changes,
        "not_performed_changes": [],
        "additional_findings": [],
        "publication_result": deepcopy(publication_result),
        "recommended_review_days": recommended_review_days,
        "return_to": "SIMS_BLOG_MANAGER",
    }
    if next_action:
        result["next_action"] = next_action
    return result


def validate_output_contract_for_request(request: dict[str, Any], result: dict[str, Any]) -> list[str]:
    """Final Contract Gate. Returns blocking issue messages."""
    expected_fmt, expected_ver = expected_output_contract(request)
    issues: list[str] = []
    if result.get("format") != expected_fmt:
        issues.append(f"output format must be {expected_fmt}; got {result.get('format') or 'missing'}")
    if str(result.get("contract_version") or "") != str(expected_ver):
        issues.append(f"contract_version must be {expected_ver}; got {result.get('contract_version') or 'missing'}")
    if expected_fmt == TREATMENT_RESULT_FORMAT:
        for key in ("case_id", "article_id", "treatment_status", "referral_compliance", "publication_result"):
            if key not in result:
                issues.append(f"treatment result missing required field: {key}")
        if str(result.get("case_id") or "") != str(request.get("case_id") or ""):
            issues.append("case_id must be preserved from the treatment request")
    return issues


def assert_output_contract_for_request(request: dict[str, Any], result: dict[str, Any]) -> None:
    issues = validate_output_contract_for_request(request, result)
    if issues:
        raise ValueError("; ".join(issues))
