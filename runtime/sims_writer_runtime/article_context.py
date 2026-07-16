from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen=True)
class PerformanceMetrics:
    clicks: float | None = None
    impressions: float | None = None
    ctr: float | None = None
    average_position: float | None = None


@dataclass(frozen=True)
class ArticleContext:
    request_id: str
    article_id: str | None
    request_type: str
    language: str
    target_url: str | None
    current_title: str
    seo_title: str
    meta_description: str
    main_query: str
    supporting_queries: list[str] = field(default_factory=list)
    improvement_goal: list[str] = field(default_factory=list)
    requested_output: list[str] = field(default_factory=list)
    existing_content: str = ""
    performance: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    source_system: str = "generic_json"
    schema_version: str = "1.0"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ArticleContextBuilder:
    """Build the immutable runtime context from a validated canonical request."""

    @classmethod
    def build(cls, request: dict[str, Any]) -> ArticleContext:
        performance = request.get("performance") or {}
        return ArticleContext(
            request_id=request["request_id"].strip(),
            article_id=cls._clean_optional(request.get("article_id")),
            request_type=request["request_type"],
            language=request["language"],
            target_url=cls._normalize_url(request.get("target_url")),
            current_title=(request.get("current_title") or "").strip(),
            seo_title=(request.get("seo_title") or "").strip(),
            meta_description=(request.get("meta_description") or "").strip(),
            main_query=request["main_query"].strip(),
            supporting_queries=cls._unique_strings(request.get("supporting_queries") or []),
            improvement_goal=cls._unique_strings(request.get("improvement_goal") or []),
            requested_output=cls._unique_strings(request.get("requested_output") or []),
            existing_content=(request.get("existing_content") or "").strip(),
            performance=PerformanceMetrics(
                clicks=cls._number(performance.get("clicks")),
                impressions=cls._number(performance.get("impressions")),
                ctr=cls._normalize_ctr(performance.get("ctr")),
                average_position=cls._number(performance.get("average_position")),
            ),
            source_system=request.get("source_system") or "generic_json",
            schema_version=request.get("schema_version") or "1.0",
        )

    @staticmethod
    def _clean_optional(value: Any) -> str | None:
        text = str(value).strip() if value is not None else ""
        return text or None

    @staticmethod
    def _unique_strings(values: list[Any]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for value in values:
            text = str(value).strip()
            if text and text not in seen:
                result.append(text)
                seen.add(text)
        return result

    @staticmethod
    def _number(value: Any) -> float | None:
        if value in (None, ""):
            return None
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        return float(value)

    @classmethod
    def _normalize_ctr(cls, value: Any) -> float | None:
        if value in (None, ""):
            return None
        if isinstance(value, str) and value.strip().endswith("%"):
            return cls._number(value.strip()[:-1]) / 100
        number = cls._number(value)
        if number is not None and number > 1:
            return number / 100
        return number

    @staticmethod
    def _normalize_url(value: Any) -> str | None:
        if value in (None, ""):
            return None
        text = str(value).strip()
        parts = urlsplit(text)
        if not parts.scheme or not parts.netloc:
            return text
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, parts.query, ""))
