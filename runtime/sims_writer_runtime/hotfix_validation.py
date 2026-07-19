from __future__ import annotations

import re
from typing import Any

FORBIDDEN_SERP_CLAIMS = (
    "強調スニペット獲得", "FAQリッチリザルト獲得", "音声検索での露出",
    "Googleに拾われやす", "CTRが改善する", "CTR改善を保証",
    "主因と考えられます", "表示回数は十分なため即断",
)
NAMED_ATTRIBUTION_PATTERNS = (
    r"(?P<name>[^。\n]{2,30})(?:さん)?によると",
    r"(?P<name>[^。\n]{2,30})(?:さん)?が語る",
    r"(?P<name>[^。\n]{2,30})の(?:占術|理論|方法)に基づ",
)
UNCOMMON_LANGUAGE_CLAIMS = ("漢字（老成る）", "漢字(老成る)", "『老成る』", "「老成る」")
STRONG_CLAIMS = ("最強候補", "効果を最大化", "幸運を引き寄せ", "潜在意識に", "安全ライン")


def _text(package: dict[str, Any]) -> str:
    parts = [package.get("rendered_response"), package.get("article_text"), package.get("proposed_text")]
    return "\n".join(str(x or "") for x in parts)


def validate_hotfix(package: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    feedback = package.get("feedback") or {}
    if feedback.get("format") != "SIMS_FEEDBACK_V2" or feedback.get("version") != "2.0":
        issues.append("VAL-JSON-001")
    if package.get("input_article_id") and feedback.get("article_id") != package.get("input_article_id"):
        issues.append("VAL-ID-001")
    if package.get("input_article_url") and feedback.get("article_url") != package.get("input_article_url"):
        issues.append("VAL-ID-001")

    text = _text(package)
    if re.search(r"<(?:div|pre|code)\b|\bstyle\s*=", text, re.I):
        issues.append("VAL-PRESENTATION-001")
    if any(x in text for x in FORBIDDEN_SERP_CLAIMS):
        issues.append("VAL-SERP-001")

    answers = [str(x).strip() for x in package.get("canonical_answers", []) if str(x).strip()]
    if len(set(answers)) > 1:
        issues.append("VAL-ANSWER-001")

    selected = str((feedback.get("new_values") or {}).get("main_query") or package.get("selected_main_query") or "").strip()
    query_metrics = package.get("query_metrics") or []
    aligned = [q for q in query_metrics if q.get("article_alignment", True) and q.get("query")]
    if selected and aligned:
        selected_row = next((q for q in aligned if str(q.get("query")).strip() == selected), None)
        best = max(aligned, key=lambda q: float(q.get("impressions") or 0))
        if selected_row and str(best.get("query")).strip() != selected:
            selected_impressions = float(selected_row.get("impressions") or 0)
            best_impressions = float(best.get("impressions") or 0)
            if best_impressions >= max(20, selected_impressions * 2):
                issues.append("VAL-MAINQUERY-001")
        elif selected_row is None:
            issues.append("VAL-MAINQUERY-001")
    if package.get("main_query_was_missing") and selected:
        issues.append("VAL-MAINQUERY-001")

    if any(x in text for x in UNCOMMON_LANGUAGE_CLAIMS) and not package.get("language_source_verified", False):
        issues.append("VAL-LANGUAGE-001")
    if re.search(r"(?:ほとんど|必ず|一般的に)[^。]{0,30}(?:意味|表記|語源)", text) and not package.get("language_source_verified", False):
        issues.append("VAL-LANGUAGE-001")

    attribution = any(re.search(pattern, text) for pattern in NAMED_ATTRIBUTION_PATTERNS)
    if attribution:
        issues.append("VAL-PERSON-ATTRIBUTION-001")
        if not package.get("verifiable_sources"):
            issues.append("VAL-SOURCE-001")

    if any(x in text for x in STRONG_CLAIMS):
        has_qualification = "効果を保証するものでは" in text or "当サイト独自" in text
        if not package.get("claim_evidence") and not has_qualification:
            issues.append("VAL-CLAIM-001")

    internal_link_eval = feedback.get("internal_link_evaluation") or {}
    if int(internal_link_eval.get("added") or 0) > 0:
        proposed = str(package.get("proposed_text") or package.get("rendered_response") or "")
        if not re.search(r"\[[^\]]+\]\(https?://[^)]+\)|<a\s+[^>]*href=|https?://", proposed, re.I):
            issues.append("VAL-INTERNAL-LINK-001")

    warnings = feedback.get("warnings") or []
    validation = feedback.get("validation") or {}
    if warnings and validation.get("result") == "PASS":
        issues.append("VAL-VALIDATION-CONSISTENCY-001")

    detected = [x for x in issues if x not in {"VAL-JSON-001", "VAL-ID-001"}]
    declared = set(validation.get("warning_rules") or []) | set(validation.get("failed_rules") or [])
    if detected and declared and not set(detected).issubset(declared):
        issues.append("VAL-VALIDATION-CONSISTENCY-001")

    return sorted(set(issues))
