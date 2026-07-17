from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from ..adapters.output_parser import extract_json


class ClaudeOutputAcceptanceError(ValueError):
    pass


@dataclass
class ClaudeOutputValidationReport:
    valid: bool
    status: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    sha256: str = ""
    normalized_output: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ClaudeOutputValidator:
    def __init__(self, repo_root: Path):
        schema_path = repo_root / "contracts" / "integrations" / "claude-output" / "claude-output.schema.json"
        self.schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.validator = Draft202012Validator(self.schema, format_checker=FormatChecker())

    def validate_text(self, text: str, request: dict[str, Any] | None = None) -> ClaudeOutputValidationReport:
        errors: list[str] = []
        warnings: list[str] = []
        try:
            payload = extract_json(text)
        except (ValueError, json.JSONDecodeError) as exc:
            return ClaudeOutputValidationReport(False, "rejected", [f"invalid_json:{exc}"])

        for error in sorted(self.validator.iter_errors(payload), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "$"
            errors.append(f"schema:{location}:{error.message}")

        if request is not None:
            self._validate_against_request(payload, request, errors, warnings)

        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return ClaudeOutputValidationReport(
            valid=not errors,
            status="accepted" if not errors else "rejected",
            errors=errors,
            warnings=warnings,
            sha256=digest,
            normalized_output=payload if not errors else None,
        )

    def validate_file(self, output_path: Path, request_path: Path | None = None) -> ClaudeOutputValidationReport:
        if not output_path.is_file():
            raise ClaudeOutputAcceptanceError(f"Claude output file not found: {output_path}")
        request = None
        if request_path is not None:
            if not request_path.is_file():
                raise ClaudeOutputAcceptanceError(f"Request context file not found: {request_path}")
            request = json.loads(request_path.read_text(encoding="utf-8"))
        return self.validate_text(output_path.read_text(encoding="utf-8"), request)

    @staticmethod
    def _validate_against_request(
        payload: dict[str, Any], request: dict[str, Any], errors: list[str], warnings: list[str]
    ) -> None:
        catalog = request.get("article_catalog") or request.get("ArticleCatalog") or []
        allowed_urls = {
            item.get("url")
            for item in catalog
            if isinstance(item, dict) and isinstance(item.get("url"), str)
        }
        for item in payload.get("internal_link_recommendations", []):
            url = item.get("url") if isinstance(item, dict) else None
            if url and url not in allowed_urls:
                errors.append(f"catalog:unknown_internal_link_url:{url}")

        supporting = request.get("supporting_queries") or request.get("SupportingQueries") or []
        supporting_set = {str(query).strip() for query in supporting if str(query).strip()}
        for item in payload.get("separate_article_candidates", []):
            query = item.get("query") if isinstance(item, dict) else None
            if query and supporting_set and query not in supporting_set:
                warnings.append(f"query:not_in_supporting_queries:{query}")

        existing_content = request.get("existing_content") or request.get("ExistingContent")
        if not existing_content and payload.get("status") == "generated":
            errors.append("safety:generated_without_existing_content")
