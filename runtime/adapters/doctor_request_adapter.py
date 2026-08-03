"""Doctor request adapter for SIMS Writer v3.1.1."""
from __future__ import annotations
from typing import Any, Dict

class DoctorRequestError(ValueError): pass

def adapt_doctor_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    if payload.get("format") != "SIMS_DOCTOR_WRITER_REQUEST_V1":
        raise DoctorRequestError("unsupported format")
    if payload.get("contract_version") != "1.0":
        raise DoctorRequestError("unsupported contract_version")
    case=payload.get("case") or {}; treatment=payload.get("treatment") or {}; article=payload.get("article") or {}
    for name,value in [("case_id",case.get("case_id")),("treatment_id",treatment.get("treatment_id")),("article_id",article.get("article_id")),("url",article.get("url"))]:
        if not value: raise DoctorRequestError(f"{name} is required")
    if treatment.get("executor") != "SIMS_WRITER":
        raise DoctorRequestError("treatment is not assigned to SIMS_WRITER")
    prohibited=set((payload.get("editing_scope") or {}).get("prohibited_actions") or [])
    return {
        "source_system":"SIMS_DOCTOR",
        "site":payload.get("site") or {},
        "article":article,
        "case_id":case["case_id"],
        "treatment_id":treatment["treatment_id"],
        "treatment_type":treatment.get("treatment_type"),
        "diagnosis_context":payload.get("diagnosis_context") or {},
        "editing_scope":payload.get("editing_scope") or {},
        "protection":payload.get("protection") or {},
        "related_articles":payload.get("related_articles") or [],
        "intent_assignment":payload.get("intent_assignment") or {},
        "hard_prohibitions":sorted(prohibited | {"CHANGE_URL","DELETE_ARTICLE","NOINDEX"}),
        "return_contract":payload.get("return_contract") or {}
    }
