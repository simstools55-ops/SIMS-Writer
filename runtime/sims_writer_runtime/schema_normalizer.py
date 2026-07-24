from __future__ import annotations
from copy import deepcopy
from typing import Any

LEGACY_FIELDS={"version","diagnosis_code","change_flags"}
STATUSES={"proposed","approved","implemented","not_implemented","not_applicable"}

def _clean(value: Any) -> Any:
    if isinstance(value,str):
        value=value.strip()
        return value if value else None
    if isinstance(value,list):
        out=[]
        for item in value:
            cleaned=_clean(item)
            if cleaned is not None: out.append(cleaned)
        return out
    if isinstance(value,dict):
        return {k:_clean(v) for k,v in value.items() if _clean(v) is not None}
    return value

def _confidence(value: Any, default: str="low") -> str:
    text=str(value or "").strip().lower()
    if "high" in text: return "high"
    if "medium" in text: return "medium"
    if "low" in text: return "low"
    return default

def normalize_feedback(payload: dict[str,Any]) -> dict[str,Any]:
    p=_clean(deepcopy(payload))
    p.pop("version",None)
    p["format"]="SIMS_FEEDBACK_V2"
    p["contract_version"]="2.1"
    if "url" in p and "article_url" not in p: p["article_url"]=p.pop("url")
    if "risk" in p and "risk_level" not in p: p["risk_level"]=p.pop("risk")

    raw=p.pop("diagnosis_code",None) or p.get("diagnosis") or "UNKNOWN"
    if isinstance(raw,str):
        diagnosis={"code":raw,"confidence":_confidence(p.pop("diagnosis_confidence",None),_confidence(p.get("confidence"),"medium")),"reasons":p.pop("diagnosis_reasons",None) or []}
    else:
        diagnosis={"code":raw.get("code") or "UNKNOWN","confidence":_confidence(raw.get("confidence"),_confidence(p.get("confidence"),"medium")),"reasons":raw.get("reasons") or []}
        for key in ("main_query","main_query_source","sample_size_flag"):
            if raw.get(key) is not None: diagnosis[key]=raw[key]
    p["diagnosis"]=diagnosis

    embedded_qc=raw.get("query_coverage") if isinstance(raw,dict) else None
    qc=p.get("query_coverage") or embedded_qc or {}
    p["query_coverage"]={
      "captured_impressions":qc.get("captured_impressions"),"total_impressions":qc.get("total_impressions"),"coverage_percent":qc.get("coverage_percent"),
      "coverage_confidence":_confidence(qc.get("coverage_confidence") or qc.get("confidence_level") or qc.get("confidence")),
      "primary":qc.get("primary") or [],"secondary":qc.get("secondary") or [],"adjacent":qc.get("adjacent") or [],"separate_article":qc.get("separate_article") or []}
    p["query_coverage"]={k:v for k,v in p["query_coverage"].items() if v is not None}

    flags=p.pop("change_flags",None) or {}
    new_values=p.get("new_values") or {}
    changes=p.get("changes")
    if not isinstance(changes,list):
        changes=[]
        for target,changed in flags.items():
            if changed:
                changes.append({"target":target,"implementation_status":"implemented","before":None,"after":new_values.get(target),"reason":"normalized from legacy change_flags"})
    normalized=[]
    for item in changes:
        if not isinstance(item,dict): continue
        status=item.get("implementation_status") or item.get("status") or "implemented"
        if status not in STATUSES: status="implemented"
        normalized.append({"target":item.get("target") or item.get("component") or "unknown","implementation_status":status,"before":item.get("before"),"after":item.get("after"),"reason":item.get("reason")})
    p["changes"]=normalized

    if isinstance(new_values,dict): p["new_values"]={k:v for k,v in new_values.items() if v is not None and v!=""}
    effect=p.get("expected_effect")
    if isinstance(effect,dict): p["expected_effect"]={k:v for k,v in effect.items() if v is not None and v!=""}

    val=p.get("validation") or {}
    checks=val.get("checks") or []
    passed=list(val.get("passed_rules") or [])
    failed=list(val.get("failed_rules") or [])
    warned=list(val.get("warning_rules") or [])
    for check in checks:
        if not isinstance(check,dict) or not check.get("code"): continue
        status=str(check.get("status") or "").upper()
        bucket=passed if status=="PASS" else failed if status=="FAIL" else warned
        if check["code"] not in bucket: bucket.append(check["code"])
    p["validation"]={"result":val.get("result") or val.get("status") or "UNVERIFIABLE","checks":checks,"failed_rules":failed,"warning_rules":warned,"passed_rules":passed,"notes":val.get("notes") or []}

    p["warnings"]=p.get("warnings") or []
    p["information"]=p.get("information") or []
    p["protected_elements"]=p.get("protected_elements") or (p.get("swls") or {}).get("protected_elements") or []
    if "confidence" in p: p["confidence"]=_confidence(p["confidence"],"medium")
    if not p.get("implementation_status"):
        statuses=[x["implementation_status"] for x in normalized]
        p["implementation_status"]="implemented" if "implemented" in statuses else "proposed" if normalized else "not_applicable"
    return p

def legacy_fields(payload: dict[str,Any]) -> list[str]:
    return sorted(LEGACY_FIELDS.intersection(payload))
