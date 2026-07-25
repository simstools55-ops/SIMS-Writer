from __future__ import annotations
from typing import Any
from .schema_normalizer import _validation_message

def enforce_validation_messages(payload: dict[str, Any]) -> dict[str, Any]:
    validation=payload.setdefault("validation",{})
    checks=validation.setdefault("checks",[])
    violations=[]
    for index,check in enumerate(checks):
        if not isinstance(check,dict):
            violations.append(f"validation.checks[{index}] is not an object")
            continue
        code=str(check.get("code") or "VAL-UNKNOWN-001")
        status=str(check.get("status") or "UNVERIFIABLE").upper()
        check["code"]=code
        check["status"]=status
        check["message"]=_validation_message(code,status,check.get("message"))
        if not check["message"].strip():
            violations.append(f"validation.checks[{index}].message is blank")
    if violations:
        validation["result"]="FAIL"
        validation.setdefault("failed_rules",[]).append("VAL-CONTRACT-006")
        raise ValueError("; ".join(violations))
    return payload

def blank_validation_messages(payload: dict[str,Any]) -> list[str]:
    issues=[]
    for index,check in enumerate((payload.get("validation") or {}).get("checks") or []):
        if not isinstance(check,dict) or not str(check.get("message") or "").strip():
            issues.append(f"validation.checks[{index}].message")
    return issues
