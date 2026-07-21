from __future__ import annotations

import re
from typing import Any

_ANXIETY_TERMS = {
    "safety": ("安全", "危険", "詐欺", "怪しい", "大丈夫"),
    "billing": ("解約", "返金", "返品", "課金", "継続", "料金", "無料"),
    "compatibility": ("使える", "対応", "iphone", "android", "windows", "suica"),
    "reliability": ("口コミ", "評判", "信頼", "精度", "本当"),
}
_ENTITY_PATTERNS = (
    r"Windows\s*11", r"iPhone", r"Android", r"Discord", r"Notion", r"Suica",
    r"Wi-?Fi(?:\s*7)?", r"[A-Za-z][A-Za-z0-9+._-]{2,}", r"「[^」]{2,40}」",
)
_TOKEN_RE = re.compile(r"[一-龥ぁ-んァ-ヶA-Za-z0-9]+")


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return " ".join(_text(v) for v in value)
    if isinstance(value, dict):
        return " ".join(_text(v) for v in value.values())
    return str(value)


def _tokens(value: Any) -> set[str]:
    return {t.lower() for t in _TOKEN_RE.findall(_text(value)) if len(t) >= 2}


def detect_intent_gap(request: dict[str, Any]) -> dict[str, Any]:
    query = _text(request.get("main_query")).strip()
    subject = " ".join(filter(None, [
        _text(request.get("seo_title")), _text(request.get("current_title")),
        _text(request.get("existing_content"))[:3000],
    ]))
    if not query or not subject:
        return {"detected": False, "level": "NOT_AVAILABLE", "reason": "query_or_subject_missing"}
    q = _tokens(query)
    s = _tokens(subject)
    overlap = len(q & s) / max(1, len(q))
    level = "LOW" if overlap >= .67 else "MEDIUM" if overlap >= .34 else "HIGH"
    return {
        "detected": level != "LOW",
        "level": level,
        "expected_answer": query,
        "actual_subject": request.get("seo_title") or request.get("current_title") or "",
        "resolution": "導入・見出し・FAQの最小範囲で不足回答を補う" if level != "LOW" else "no_change",
        "token_coverage": round(overlap, 3),
    }


def detect_hidden_anxiety(request: dict[str, Any]) -> dict[str, Any]:
    queries = [_text(request.get("main_query")), *_as_list(request.get("supporting_queries"))]
    article = _text(request.get("existing_content"))
    found=[]
    for category, terms in _ANXIETY_TERMS.items():
        matched_terms = {t for q in queries for t in terms if t.lower() in q.lower()}
        evidence=[q for q in queries if any(t.lower() in q.lower() for t in matched_terms)]
        if not evidence:
            continue
        unanswered_terms=[t for t in matched_terms if t.lower() not in article.lower()]
        if unanswered_terms:
            found.append({"category": category, "evidence": evidence[:3], "unanswered_terms": sorted(unanswered_terms), "answered": False})
    return {"detected": bool(found), "items": found, "application": "unanswered_and_decision_relevant_only"}


def extract_serp_entities(request: dict[str, Any]) -> dict[str, Any]:
    source=" ".join([_text(request.get("main_query")), _text(request.get("seo_title")), _text(request.get("current_title"))])
    entities=[]
    for pattern in _ENTITY_PATTERNS:
        for item in re.findall(pattern, source, flags=re.I):
            value=item if isinstance(item, str) else "".join(item)
            value=value.strip()
            if value and value.lower() not in {e.lower() for e in entities}:
                entities.append(value)
    return {"protected_entities": entities, "policy": "preserve_search_context_unless_replacement_is_explicitly_justified"}


def evaluate_internal_links(request: dict[str, Any]) -> dict[str, Any]:
    catalog=request.get("article_catalog") or []
    intent_tokens=_tokens([request.get("main_query"), request.get("supporting_queries")])
    evaluated=[]
    for item in catalog:
        if not isinstance(item, dict):
            continue
        candidate_tokens=_tokens([item.get("title"), item.get("main_query"), item.get("queries"), item.get("summary")])
        overlap=len(intent_tokens & candidate_tokens) / max(1, len(intent_tokens))
        same_url=bool(item.get("url") and item.get("url") == request.get("target_url"))
        url_verified=bool(item.get("url"))
        decision="adopt" if overlap >= .34 and url_verified and not same_url else "hold" if overlap >= .17 and url_verified and not same_url else "reject"
        evaluated.append({"article_id": item.get("article_id") or item.get("ArticleID"), "url": item.get("url") or item.get("ArticleURL"), "semantic_score": round(overlap,3), "decision": decision})
    return {"evaluated": evaluated, "policy": "semantic_complementarity_over_string_similarity"}


def classify_evidence(request: dict[str, Any]) -> dict[str, Any]:
    sources=request.get("source_evidence") or []
    counts={"official":0,"independent_third_party":0,"user_generated":0,"search_snippet":0,"unverified":0}
    for source in sources:
        kind=_text(source.get("type") if isinstance(source,dict) else source).lower()
        if "official" in kind or "公式" in kind: counts["official"] += 1
        elif "third" in kind or "第三者" in kind: counts["independent_third_party"] += 1
        elif "review" in kind or "口コミ" in kind or "blog" in kind: counts["user_generated"] += 1
        elif "snippet" in kind or "スニペット" in kind: counts["search_snippet"] += 1
        else: counts["unverified"] += 1
    confidence="HIGH" if counts["official"] and counts["unverified"] == 0 else "MEDIUM" if counts["official"] or counts["independent_third_party"] else "LOW"
    return {"counts":counts,"confidence":confidence,"assertion_policy":"do_not_exceed_evidence_strength"}


def build_editorial_signals(request: dict[str, Any]) -> dict[str, Any]:
    return {
        "intent_gap": detect_intent_gap(request),
        "hidden_anxiety": detect_hidden_anxiety(request),
        "serp_entity_preservation": extract_serp_entities(request),
        "internal_link_semantics": evaluate_internal_links(request),
        "evidence_transparency": classify_evidence(request),
        "decision_support_policy": "propose_only_when_equivalent_support_is_missing",
        "preservation_guard": "signals_do_not_override_preservation_score_change_budget_or_rewrite_scope",
    }


def _as_list(value: Any) -> list[str]:
    if value is None: return []
    if isinstance(value, list): return [_text(v) for v in value]
    return [_text(value)]
