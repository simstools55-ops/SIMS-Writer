from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


class RequestValidationError(ValueError):
    """Raised when an improvement request cannot be parsed or validated."""


@dataclass(frozen=True)
class LoadedRequest:
    payload: dict[str, Any]
    input_type: str
    schema_version: str
    source_path: str | None = None


class ImprovementRequestLoader:
    """Load and validate SIMS Writer improvement requests.

    Supported sources:
    - Python dictionaries
    - UTF-8 JSON files
    - SIMS-Blog-Manager JSON (PascalCase fields)
    - Generic SIMS Writer JSON (snake_case fields)
    """

    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root)
        schema_path = self.repo_root / "contracts/request/improvement-request/improvement-request.schema.json"
        self.schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.validator = Draft202012Validator(self.schema)

    def load(self, source: dict[str, Any] | str | Path, input_type: str = "auto") -> LoadedRequest:
        source_path: str | None = None
        if isinstance(source, dict):
            payload = source
        else:
            path = Path(source)
            source_path = str(path.resolve())
            try:
                payload = json.loads(path.read_text(encoding="utf-8-sig"))
            except FileNotFoundError as exc:
                raise RequestValidationError(f"Request file not found: {path}") from exc
            except json.JSONDecodeError as exc:
                raise RequestValidationError(
                    f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
                ) from exc
        if not isinstance(payload, dict):
            raise RequestValidationError("Request root must be a JSON object")

        detected = self.detect_input_type(payload) if input_type == "auto" else input_type
        if detected not in {"generic", "sbm"}:
            raise RequestValidationError(f"Unsupported input type: {detected}")

        canonical = self._sanitize_canonical(self._to_canonical(payload, detected))
        errors = sorted(self.validator.iter_errors(canonical), key=lambda error: list(error.path))
        if errors:
            details = "; ".join(self._format_error(error) for error in errors)
            raise RequestValidationError(f"Request schema validation failed: {details}")
        return LoadedRequest(
            payload=canonical,
            input_type=detected,
            schema_version=canonical["schema_version"],
            source_path=source_path,
        )

    @staticmethod
    def detect_input_type(payload: dict[str, Any]) -> str:
        sbm_markers = {"RequestID", "ArticleID", "URL", "MainQuery"}
        generic_markers = {"request_id", "article_id", "target_url", "main_query"}
        if sbm_markers.intersection(payload):
            return "sbm"
        if generic_markers.intersection(payload) or "payload" in payload:
            return "generic"
        raise RequestValidationError("Unable to detect request format")

    def _to_canonical(self, payload: dict[str, Any], input_type: str) -> dict[str, Any]:
        if input_type == "generic" and isinstance(payload.get("payload"), dict):
            payload = payload["payload"]
        if input_type == "sbm":
            performance = {
                "clicks": payload.get("Clicks"),
                "impressions": payload.get("Impressions"),
                "ctr": payload.get("CTR"),
                "average_position": payload.get("AveragePosition"),
            }
            return {
                "schema_version": str(payload.get("SchemaVersion") or "1.0"),
                "request_id": payload.get("RequestID"),
                "article_id": payload.get("ArticleID"),
                "request_type": "existing_article_improvement",
                "language": payload.get("Language") or "ja-JP",
                "target_url": payload.get("URL"),
                "current_title": payload.get("ArticleTitle") or "",
                "seo_title": payload.get("SEOTitle") or "",
                "meta_description": payload.get("MetaDescription") or "",
                "main_query": payload.get("MainQuery"),
                "supporting_queries": payload.get("SupportingQueries") or [],
                "improvement_goal": payload.get("ImprovementGoal") or [],
                "requested_output": payload.get("RequestedOutput") or ["publication_package", "before_after"],
                "existing_content": payload.get("ExistingContent") or payload.get("ArticleContent") or "",
                "content_format": payload.get("ContentFormat") or payload.get("ArticleContentFormat") or "auto",
                "performance": {k: v for k, v in performance.items() if v is not None},
                "source_system": "sims_blog_manager",
            }
        query = payload.get("query") if isinstance(payload.get("query"), dict) else {}
        article = payload.get("article") if isinstance(payload.get("article"), dict) else {}
        request_type = payload.get("request_type") or "existing_article_improvement"
        default_goal = ["new_article_creation"] if request_type == "new_article" else ["article_improvement"]
        return {
            "schema_version": str(payload.get("schema_version") or "1.0"),
            "request_id": payload.get("request_id"),
            "article_id": payload.get("article_id") or article.get("article_id"),
            "request_type": request_type,
            "language": payload.get("language") or "ja-JP",
            "target_url": payload.get("target_url") or article.get("target_url"),
            "current_title": payload.get("current_title") or payload.get("title") or article.get("title") or "",
            "seo_title": payload.get("seo_title") or "",
            "meta_description": payload.get("meta_description") or "",
            "main_query": payload.get("main_query") or query.get("main_query"),
            "supporting_queries": payload.get("supporting_queries") or query.get("supporting_queries") or [],
            "improvement_goal": payload.get("improvement_goal") or default_goal,
            "requested_output": payload.get("requested_output") or ["publication_package"],
            "existing_content": payload.get("existing_content") or payload.get("article_content") or "",
            "content_format": payload.get("content_format") or "auto",
            "performance": payload.get("performance") or {},
            "source_system": payload.get("source_system") or "generic_json",
        }

    @classmethod
    def _sanitize_canonical(cls, canonical: dict[str, Any]) -> dict[str, Any]:
        cleaned = dict(canonical)
        for field in ("supporting_queries", "improvement_goal", "requested_output"):
            values = cleaned.get(field) or []
            unique: list[str] = []
            seen: set[str] = set()
            for value in values:
                text = str(value).strip()
                if text and text not in seen:
                    unique.append(text)
                    seen.add(text)
            cleaned[field] = unique
        performance = dict(cleaned.get("performance") or {})
        for field in ("clicks", "impressions", "average_position"):
            performance[field] = cls._parse_number(performance.get(field))
        performance["ctr"] = cls._parse_ctr(performance.get("ctr"))
        cleaned["performance"] = {key: value for key, value in performance.items() if value is not None}
        return cleaned

    @staticmethod
    def _parse_number(value: Any) -> float | None:
        if value in (None, ""):
            return None
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        try:
            return float(value)
        except (TypeError, ValueError) as exc:
            raise RequestValidationError(f"Performance value must be numeric: {value}") from exc

    @classmethod
    def _parse_ctr(cls, value: Any) -> float | None:
        if value in (None, ""):
            return None
        if isinstance(value, str) and value.strip().endswith("%"):
            return cls._parse_number(value.strip()[:-1]) / 100
        number = cls._parse_number(value)
        return number / 100 if number is not None and number > 1 else number

    @staticmethod
    def _format_error(error: Any) -> str:
        location = ".".join(str(part) for part in error.path) or "$"
        return f"{location}: {error.message}"
