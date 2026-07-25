from __future__ import annotations
from copy import deepcopy
from typing import Any
import re

LEGACY_FIELDS={"version","diagnosis_code","change_flags"}
STATUSES={"proposed","approved","implemented","not_implemented","not_applicable","held"}
COMPONENT_ALIASES={"target":"component","description":"meta_description","seo_description":"meta_description"}

VALIDATION_MESSAGE_DEFAULTS={
    'VAL-CONTRACT-001': '必須項目・型・命名がContract 2.1に整合することを確認',
    'VAL-INTENT-001': '主要検索意図が変更前後で維持されていることを確認',
    'VAL-PRESERVE-001': '保護対象一覧と差分を照合し、未承認の変更がないことを確認',
    'VAL-BUDGET-001': '推定変更率が設定された変更量の上限以内であることを確認',
    'VAL-SCOPE-001': '宣言した修正範囲と実際の変更項目が一致することを確認',
    'VAL-FACT-001': '数値・日付・仕様に矛盾や未確認の追加がないことを確認',
    'VAL-EVIDENCE-001': '主張と変更内容が確認できた根拠範囲内であることを確認',
    'VAL-EVIDENCE-002': '確認できた証拠を超える事実や断定がないことを確認',
    'VAL-CAUSAL-001': '未確認の因果関係・同一視・効果保証がないことを確認',
    'VAL-CONSISTENCY-001': '各コンポーネント間で主張の矛盾がないことを確認',
    'VAL-ENTITY-001': 'Entityエンコードと文字コードに異常がないことを確認',
    'VAL-LINK-001': 'リンクのURL・アンカー・採否・実装状態が一致することを確認',
    'VAL-TITLE-001': 'タイトルの長さと本文への約束が公開基準に適合することを確認',
    'VAL-META-001': 'メタの長さと内容が本文の根拠範囲に適合することを確認',
    'VAL-FAQ-001': 'FAQが重複ではなく残存疑問へ正確に回答することを確認',
    'VAL-SAMPLE-001': 'データ量に応じて確信度と変更範囲を抑制したことを確認',
    'VAL-MAINQUERY-001': 'メインクエリの入力・推定根拠・採用状態を確認',
    'VAL-LANG-001': '利用者向け出力が日本語中心で不要な英語説明がないことを確認',
 }

def _validation_message(code: str, status: str, existing: Any=None) -> str:
    message=str(existing or "").strip()
    generic={f"{code} の確認を完了", "確認済み", "PASS", "OK", "問題なし"}
    if message and message not in generic:
        return message
    if code in VALIDATION_MESSAGE_DEFAULTS:
        return VALIDATION_MESSAGE_DEFAULTS[code]
    normalized_status=(status or "UNVERIFIABLE").upper()
    return f"{code}を{normalized_status}として判定した具体的な確認内容を記録"

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

def _compact_trace_item(item: dict[str, Any], fallback_cycle: int) -> dict[str, Any]:
    cycle=int(item.get("cycle") or fallback_cycle)
    checked=item.get("checked") or item.get("focus") or []
    if isinstance(checked,str):
        checked=[x.strip() for x in re.split(r"[、,/・]+", checked) if x.strip()]
    findings=item.get("findings") or ([item.get("finding")] if item.get("finding") else [])
    actions=item.get("actions") or ([item.get("action")] if item.get("action") else [])
    if isinstance(findings,str): findings=[findings]
    if isinstance(actions,str): actions=[actions]
    out={"cycle":cycle,"checked":checked or ["publication_qa"]}
    if findings: out["findings"]=findings
    if actions: out["actions"]=actions
    out["result"]=item.get("result") or "recorded"
    return out

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
                changes.append({"component":target,"implementation_status":"implemented","after":new_values.get(target),"reason":"normalized from legacy change_flags"})
    normalized=[]
    for item in changes:
        if not isinstance(item,dict): continue
        status=item.get("implementation_status") or item.get("status") or "implemented"
        if status not in STATUSES: status="implemented"
        if status in {"not_implemented", "not_applicable"}:
            continue
        component=item.get("component") or item.get("target") or "unknown"
        if component in {"description","seo_description"}: component="meta_description"
        change={"component":component,"implementation_status":status}
        if item.get("before") not in (None, ""): change["before"]=item.get("before")
        if item.get("after") not in (None, ""): change["after"]=item.get("after")
        if item.get("reason") not in (None, ""): change["reason"]=item.get("reason")
        normalized.append(change)
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
        status=str(check.get("status") or "UNVERIFIABLE").upper()
        check["message"]=_validation_message(str(check["code"]),status,check.get("message"))
        bucket=passed if status=="PASS" else failed if status=="FAIL" else warned
        if check["code"] not in bucket: bucket.append(check["code"])
    p["validation"]={"result":val.get("result") or val.get("status") or "UNVERIFIABLE","checks":checks,"failed_rules":failed,"warning_rules":warned,"passed_rules":passed,"notes":val.get("notes") or []}


    ile=p.get("internal_link_evaluation")
    if isinstance(ile,dict):
        p["internal_link_evaluation_summary"]=_clean(ile)
        p["internal_link_evaluation"]=[]
    elif not isinstance(ile,list):
        p["internal_link_evaluation"]=[]


    # Canonical top-level main_query and aliases.
    if not p.get("main_query"):
        mq=(p.get("diagnosis") or {}).get("main_query")
        if mq: p["main_query"]=mq
    if isinstance(p.get("new_values"),dict) and "description" in p["new_values"] and "meta_description" not in p["new_values"]:
        p["new_values"]["meta_description"]=p["new_values"].pop("description")

    # Canonical Publication QA. Legacy fields may be accepted as input but never emitted as the primary form.
    qa=p.get("publication_qa") or {}
    if isinstance(qa,dict) and qa:
        qa["contract"]="SIMS_EDITORIAL_QA_V1"
        legacy_fix=qa.pop("auto_fix_applied",None)
        fixes=qa.get("auto_fixes")
        if not isinstance(fixes,list):
            fixes=[]
        if legacy_fix is True and not fixes:
            fixes=[{"rule":"LEGACY_AUTO_FIX","component":"unknown","action":"legacy_auto_fix_recorded"}]
        qa["auto_fixes"]=fixes
        trace=qa.get("review_trace")
        if isinstance(trace,str):
            trace=[{"cycle":1,"checked":["publication_qa"],"actions":[trace],"result":qa.get("final_verdict") or "UNKNOWN"}]
        elif isinstance(trace,list):
            converted=[]
            for idx,item in enumerate(trace,1):
                if isinstance(item,dict): converted.append(_compact_trace_item(item,idx))
                else: converted.append({"cycle":idx,"checked":["publication_qa"],"actions":[str(item)],"result":"recorded"})
            trace=converted
        else: trace=[]
        qa["review_trace"]=trace
        if trace:
            qa["review_cycles_used"]=max(int(x.get("cycle") or 0) for x in trace)
        for fix in qa.get("auto_fixes") or []:
            if isinstance(fix,dict) and "target" in fix and "component" not in fix:
                fix["component"]=fix.pop("target")
        unresolved=qa.get("unresolved_findings") or []
        structured=[]
        for item in unresolved:
            if isinstance(item,dict): structured.append(item)
            else: structured.append({"item":str(item),"severity":"info","blocking":False,"status":"pending_verification","detail":str(item)})
        qa["unresolved_findings"]=structured
        if structured and qa.get("final_verdict")=="PASS":
            qa["final_verdict"]="PASS_WITH_WARNING"
            qa["release_action"]="publish_with_advisory"
        p["publication_qa"]=_clean(qa)

    # Candidate-level internal-link evaluation aliases.
    normalized_links=[]
    for item in p.get("internal_link_evaluation") or []:
        if not isinstance(item,dict): continue
        decision=item.get("decision") or item.get("status") or "held"
        normalized_links.append({
            "title": item.get("title") or item.get("candidate"),
            "url": item.get("url") or item.get("candidate_url"),
            "decision": decision,
            "implementation_status": "implemented" if decision=="adopted" else "not_implemented",
            "reason": item.get("reason") or "評価理由未記載",
        })
    p["internal_link_evaluation"]=_clean(normalized_links)

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
