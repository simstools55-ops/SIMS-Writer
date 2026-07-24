from __future__ import annotations
from copy import deepcopy
from typing import Any
EMPTY_ARRAY_FIELDS={"warnings","information","protected_elements"}
def _clean(v):
    if isinstance(v,str): return v.strip() or None
    if isinstance(v,list): return [_clean(x) for x in v if _clean(x) is not None]
    if isinstance(v,dict): return {k:_clean(x) for k,x in v.items()}
    return v
def normalize_feedback(payload: dict[str,Any]) -> dict[str,Any]:
    p=_clean(deepcopy(payload))
    p["format"]="SIMS_FEEDBACK_V2"; p["contract_version"]="2.1"
    raw=p.pop("diagnosis_code",None) or p.get("diagnosis") or "UNKNOWN"
    if isinstance(raw,str): p["diagnosis"]={"code":raw,"confidence":p.pop("diagnosis_confidence",None) or "medium","reasons":p.pop("diagnosis_reasons",None) or []}
    elif isinstance(raw,dict): p["diagnosis"]={"code":raw.get("code") or "UNKNOWN","confidence":raw.get("confidence") or "medium","reasons":raw.get("reasons") or []}
    flags=p.pop("change_flags",None) or {}
    if not isinstance(p.get("changes"),list):
        p["changes"]=[{"target":k,"status":"implemented" if v else "not_applicable","before":None,"after":None,"reason":"normalized from legacy change_flags"} for k,v in flags.items()]
    for c in p.get("changes",[]): c.setdefault("status","implemented"); c.setdefault("before",None); c.setdefault("after",None); c.setdefault("reason","")
    qc=p.get("query_coverage") or {}; p["query_coverage"]={"confidence":qc.get("confidence") or "low","primary":qc.get("primary") or [],"secondary":qc.get("secondary") or [],"adjacent":qc.get("adjacent") or [],"separate_article":qc.get("separate_article") or []}
    val=p.get("validation") or {}; p["validation"]={"result":val.get("result") or "UNVERIFIABLE","failed_rules":val.get("failed_rules") or [],"warning_rules":val.get("warning_rules") or [],"passed_rules":val.get("passed_rules") or []}
    p.setdefault("implementation_status","implemented" if any(c.get("status")=="implemented" for c in p["changes"]) else "proposed")
    for k in EMPTY_ARRAY_FIELDS: p[k]=p.get(k) or []
    p.setdefault("risk_level",p.pop("risk",None) or "LOW")
    return p
