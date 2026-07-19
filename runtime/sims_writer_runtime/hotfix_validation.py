from __future__ import annotations

import re
from typing import Any

FORBIDDEN_SERP_CLAIMS = (
    "強調スニペット獲得", "FAQリッチリザルト獲得", "音声検索での露出",
    "Googleに拾われやす", "CTRが改善する", "CTR改善を保証",
)

def validate_hotfix(package: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    feedback = package.get("feedback") or {}
    if feedback.get("format") != "SIMS_FEEDBACK_V2" or feedback.get("version") != "2.0":
        issues.append("VAL-JSON-001")
    if package.get("input_article_id") and feedback.get("article_id") != package.get("input_article_id"):
        issues.append("VAL-ID-001")
    if package.get("input_article_url") and feedback.get("article_url") != package.get("input_article_url"):
        issues.append("VAL-ID-001")
    text = str(package.get("rendered_response") or "")
    if re.search(r"<(?:div|pre|code)\b|\bstyle\s*=", text, re.I):
        issues.append("VAL-PRESENTATION-001")
    if any(x in text for x in FORBIDDEN_SERP_CLAIMS):
        issues.append("VAL-SERP-001")
    answers = [str(x).strip() for x in package.get("canonical_answers", []) if str(x).strip()]
    if len(set(answers)) > 1:
        issues.append("VAL-ANSWER-001")
    return sorted(set(issues))
