from __future__ import annotations

from datetime import date, datetime
from typing import Any

SOURCE_WEIGHTS = {
    "OFFICIAL": 100,
    "PRIMARY": 92,
    "MULTIPLE_THIRD_PARTY": 75,
    "SINGLE_THIRD_PARTY": 58,
    "COMMUNITY": 38,
    "UNKNOWN": 0,
}


def source_level(record: dict[str, Any]) -> str:
    level = str(record.get("source_level") or record.get("evidence_source_level") or "UNKNOWN").upper()
    return level if level in SOURCE_WEIGHTS else "UNKNOWN"


def freshness_status(record: dict[str, Any], *, today: date | None = None) -> str:
    explicit = str(record.get("freshness_status") or "").lower()
    if explicit in {"current", "aging", "stale", "unknown", "not_applicable"}:
        return explicit
    checked = record.get("verified_at") or record.get("last_verified_at")
    if not checked:
        return "unknown"
    try:
        dt = datetime.fromisoformat(str(checked).replace("Z", "+00:00")).date()
    except ValueError:
        try: dt = date.fromisoformat(str(checked)[:10])
        except ValueError: return "unknown"
    age=((today or date.today())-dt).days
    max_age=int(record.get("max_age_days") or 365)
    if age <= max_age: return "current"
    if age <= max_age*2: return "aging"
    return "stale"


def knowledge_confidence(record: dict[str, Any], *, today: date | None = None) -> int:
    explicit=record.get("knowledge_confidence")
    if explicit is not None:
        return max(0,min(100,int(explicit)))
    score=SOURCE_WEIGHTS[source_level(record)]
    fresh=freshness_status(record,today=today)
    score += {"current":0,"not_applicable":0,"aging":-15,"stale":-35,"unknown":-20}[fresh]
    if record.get("contradicted"): score=min(score,20)
    if record.get("corroborated_by_official"): score=max(score,95)
    return max(0,min(100,score))


def publication_ceiling(record: dict[str, Any], *, today: date | None = None) -> str:
    level=source_level(record); fresh=freshness_status(record,today=today); score=knowledge_confidence(record,today=today)
    if record.get("contradicted") or score < 40 or fresh == "stale": return "INTERNAL_REJECT"
    if level in {"OFFICIAL","PRIMARY"} and fresh in {"current","not_applicable"} and score >= 85: return "PUBLIC_OK"
    if level == "MULTIPLE_THIRD_PARTY" and fresh == "current" and score >= 70: return "INTERNAL_REJECT"
    if score >= 55 and fresh in {"current","aging"}: return "INTERNAL_REJECT"
    return "INTERNAL_REJECT"
