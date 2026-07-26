from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable

YMYL_DOMAINS = {"health", "medical", "finance", "legal", "safety"}

@dataclass(frozen=True)
class FinalQualityIssue:
    code: str
    message: str
    severity: str = "error"


def _texts(values: Iterable[Any]) -> str:
    return "\n".join(str(v or "") for v in values)


def validate_title_semantics(title: str, *, body_text: str = "") -> list[FinalQualityIssue]:
    """Detect semantically invalid title constructions before publication.

    This is deliberately conservative. It blocks a small set of high-risk
    constructions and relies on explicit alignment metadata for broad claims.
    """
    issues: list[FinalQualityIssue] = []
    normalized = re.sub(r"[，,]", "", str(title or ""))
    # A numeric limit/count must not become the direct object of an action that
    # changes capacity when the article only explains workarounds.
    if re.search(r"\d[\d,]*(?:枚|個|本|件|GB|MB)を(?:実質的に)?増やす", normalized):
        issues.append(FinalQualityIssue(
            "VAL-TITLE-SEMANTIC-001",
            "A limit/count is incorrectly used as the object of 'increase'; separate the limit fact from the workaround claim.",
        ))
    # Claims framed as a numbered list must be supported by the article.
    m = re.search(r"(?:術|方法|対処法|コツ)(\d+)選|([0-9]+)つの(?:術|方法|対処法|コツ)", normalized)
    if m and body_text:
        expected = int(next(x for x in m.groups() if x))
        # Explicit headings/list markers are enough; do not infer exact support from length.
        markers = len(re.findall(r"(?:^|\n)\s*(?:#{2,4}\s*)?(?:方法|対処法|コツ)?\s*[1-9１-９][\.．、:：)]", body_text))
        if markers and markers < expected:
            issues.append(FinalQualityIssue(
                "VAL-EXPECTATION-002",
                f"Title promises {expected} items but only {markers} explicit items were found in the supplied body.",
            ))
    return issues


def validate_expectation_alignment(*, promises: list[str] | None, supported_promises: list[str] | None) -> list[FinalQualityIssue]:
    issues: list[FinalQualityIssue] = []
    p = [str(x).strip() for x in (promises or []) if str(x).strip()]
    supported = {str(x).strip() for x in (supported_promises or []) if str(x).strip()}
    missing = [x for x in p if x not in supported]
    if missing:
        issues.append(FinalQualityIssue(
            "VAL-EXPECTATION-001",
            "Title/meta promises are not supported by the article: " + ", ".join(missing),
        ))
    return issues


def validate_ymyl_safety(*, domain: str | None, public_text: str, safety_notes: list[str] | None,
                         evidence_level: str | None = None) -> list[FinalQualityIssue]:
    issues: list[FinalQualityIssue] = []
    d = str(domain or "").lower()
    if d not in YMYL_DOMAINS:
        return issues

    text = str(public_text or "")
    notes = _texts(safety_notes or [])
    # Strong adequacy/benefit claims require explicit evidence and scope.
    benefit_patterns = (
        r"(?:\d+分|短時間).{0,12}(?:で|なら).{0,8}十分",
        r"(?:必ず|確実に).{0,16}(?:改善|解消|治る|効果)",
        r"(?:ダイエット|心肺機能|血圧|骨密度).{0,20}(?:向上|改善|効果)",
    )
    if any(re.search(p, text) for p in benefit_patterns):
        if str(evidence_level or "").upper() not in {"OFFICIAL", "PRIMARY"}:
            issues.append(FinalQualityIssue(
                "VAL-BENEFIT-CLAIM-001",
                "A health benefit/adequacy claim lacks official or primary evidence and must be softened or moved to user decision.",
            ))

    # High-impact exercise and symptom/pain contexts require a safety note.
    high_impact = bool(re.search(r"縄跳び|ジャンプ|高強度|膝|腰|持病|痛み", text))
    safety_present = bool(re.search(r"医師|かかりつけ|専門家|無理のない|短時間から|中止", notes + "\n" + text))
    if high_impact and not safety_present:
        issues.append(FinalQualityIssue(
            "VAL-YMYL-SAFETY-001",
            "Health/safety content requires a clear, appropriately placed safety note before publication.",
        ))
    return issues


def validate_final_quality(package: dict[str, Any]) -> list[FinalQualityIssue]:
    feedback = package.get("feedback") or {}
    publication = feedback.get("publication_result") or {}
    changes = publication.get("public_ok_changes") or []
    public_text_parts: list[str] = []
    title = ""
    body_text = str(package.get("article_content") or package.get("body_text") or "")
    for change in changes:
        after = str(change.get("after") or change.get("summary") or "")
        public_text_parts.append(after)
        if str(change.get("component") or "") in {"seo_title", "article_title"}:
            title = after
    public_text = _texts(public_text_parts)

    issues: list[FinalQualityIssue] = []
    issues.extend(validate_title_semantics(title, body_text=body_text))
    alignment = package.get("content_alignment") or {}
    issues.extend(validate_expectation_alignment(
        promises=alignment.get("promises"),
        supported_promises=alignment.get("supported_promises"),
    ))
    safety = package.get("safety_context") or {}
    issues.extend(validate_ymyl_safety(
        domain=package.get("domain") or safety.get("domain"),
        public_text=public_text,
        safety_notes=safety.get("notes"),
        evidence_level=safety.get("evidence_level"),
    ))
    return issues
