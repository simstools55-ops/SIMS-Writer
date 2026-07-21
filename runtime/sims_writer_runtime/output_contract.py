from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from typing import Any
import re

from .publish_quality import validate_before_after_editorial, validate_comparison_article

USER_CONTRACT_TYPE_NAMES = {
    "string": str, "boolean": bool, "integer": int, "number": (int, float),
    "object": dict, "array": list, "null": type(None),
}

OUTPUT_MODES = {"summary", "partial", "full", "publish", "json_only"}
SEO_TITLE_RECOMMENDED_MAX = 40
SEO_TITLE_HARD_MAX = 45
META_DESCRIPTION_RECOMMENDED_MAX = 120
META_DESCRIPTION_HARD_MAX = 140
FORBIDDEN_PREFACE_PATTERNS = (
    r"^\s*(?:承知しました|了解しました|かしこまりました)[。！!]?",
    r"^\s*(?:マスター|幹事長|先生|社長|部長|課長|[ぁ-んァ-ヶ一-龠々ー]{1,12}さん)[、,]",
)
CHANGE_KEYS = (
    "article_title", "seo_title", "description", "introduction", "headings",
    "faq", "internal_links", "body", "images",
)


def validate_user_json_contract(feedback: dict[str, Any], contract: dict[str, Any]) -> list[OutputValidationIssue]:
    """Validate exact user-provided JSON contract: keys, order, required fields and types."""
    issues: list[OutputValidationIssue] = []
    expected_order = contract.get("field_order") or list((contract.get("fields") or {}).keys())
    actual_order = list(feedback.keys())
    if expected_order and actual_order != expected_order:
        issues.append(OutputValidationIssue("OUT-018", "feedback field order must exactly match the user contract"))

    fields = contract.get("fields") or {}
    expected_keys = set(fields)
    actual_keys = set(feedback)
    missing = [k for k in expected_order if k not in actual_keys]
    extra = [k for k in actual_order if k not in expected_keys]
    if missing:
        issues.append(OutputValidationIssue("OUT-019", f"feedback is missing contract fields: {', '.join(missing)}"))
    if extra:
        issues.append(OutputValidationIssue("OUT-020", f"feedback contains contract-external fields: {', '.join(extra)}"))

    def check(value: Any, spec: Any, path: str) -> None:
        if isinstance(spec, str):
            expected = USER_CONTRACT_TYPE_NAMES.get(spec)
            if expected is None:
                return
            if spec == "integer" and isinstance(value, bool):
                ok = False
            elif spec == "number" and isinstance(value, bool):
                ok = False
            else:
                ok = isinstance(value, expected)
            if not ok:
                issues.append(OutputValidationIssue("OUT-021", f"{path} must be {spec}"))
            return
        if isinstance(spec, dict):
            if not isinstance(value, dict):
                issues.append(OutputValidationIssue("OUT-021", f"{path} must be object"))
                return
            expected_nested = list(spec.keys())
            if list(value.keys()) != expected_nested:
                issues.append(OutputValidationIssue("OUT-022", f"{path} keys and order must exactly match the user contract"))
            for key, child in spec.items():
                if key not in value:
                    issues.append(OutputValidationIssue("OUT-019", f"{path}.{key} is required"))
                else:
                    check(value[key], child, f"{path}.{key}")

    for key, spec in fields.items():
        if key in feedback:
            check(feedback[key], spec, key)
    return issues


@dataclass
class OutputValidationIssue:
    code: str
    message: str
    severity: str = "error"


class OutputContractValidator:
    """Validates the human-facing result and SIMS_FEEDBACK_V2 as separate layers."""

    def validate(self, package: dict[str, Any]) -> list[OutputValidationIssue]:
        issues: list[OutputValidationIssue] = []
        mode = package.get("output_mode")
        if mode not in OUTPUT_MODES:
            issues.append(OutputValidationIssue("OUT-001", f"Unsupported output_mode: {mode}"))

        feedback = package.get("feedback")
        if not isinstance(feedback, dict):
            issues.append(OutputValidationIssue("OUT-002", "feedback must be an object"))
            return issues

        user_contract = package.get("user_json_contract")
        if isinstance(user_contract, dict):
            issues.extend(validate_user_json_contract(feedback, user_contract))

        if feedback.get("format") != "SIMS_FEEDBACK_V2":
            issues.append(OutputValidationIssue("OUT-003", "feedback.format must be SIMS_FEEDBACK_V2"))
        if feedback.get("version") != "2.0":
            issues.append(OutputValidationIssue("OUT-030", "feedback.version must be 2.0"))
        # A strict user-provided contract remains authoritative for backward compatibility.
        # Full current V2 extension fields are mandatory only under the default contract.
        if not isinstance(user_contract, dict):
            required_v2 = ("diagnosis", "primary_intent", "effect_confidence", "preservation_score",
                           "protected_elements", "change_budget_percent", "rewrite_level",
                           "rewrite_scope", "risk", "validation", "internal_link_evaluation")
            missing_v2 = [k for k in required_v2 if k not in feedback]
            if missing_v2:
                # Legacy builder output remains accepted during the v1.1 compatibility window.
                legacy_shape = all(k in feedback for k in ("completed_at", "changes", "new_values", "recommended_review_days"))
                if not legacy_shape:
                    issues.append(OutputValidationIssue("OUT-031", f"V2 fields missing: {', '.join(missing_v2)}"))

        if feedback.get("main_query_source") not in {"search_console", "manual", "estimated", "unavailable"}:
            issues.append(OutputValidationIssue("OUT-025", "main_query_source must be search_console, manual, estimated, or unavailable"))
        if feedback.get("execution_mode") not in {"standard", "graceful_degradation"}:
            issues.append(OutputValidationIssue("OUT-026", "execution_mode must be standard or graceful_degradation"))
        estimated_fields = feedback.get("estimated_fields")
        if not isinstance(estimated_fields, list) or any(not isinstance(x, str) for x in estimated_fields):
            issues.append(OutputValidationIssue("OUT-027", "estimated_fields must be an array of strings"))
        if not isinstance(feedback.get("information"), list):
            issues.append(OutputValidationIssue("OUT-028", "information must be an array"))
        if feedback.get("main_query_source") == "estimated" and "main_query" not in (estimated_fields or []):
            issues.append(OutputValidationIssue("OUT-029", "estimated main_query must be listed in estimated_fields"))

        changes = feedback.get("changes") or {}
        missing = [key for key in CHANGE_KEYS if key not in changes]
        if missing:
            issues.append(OutputValidationIssue("OUT-004", f"changes is missing: {', '.join(missing)}"))

        main_query = (feedback.get("new_values") or {}).get("main_query", "")
        if any(token in str(main_query) for token in ("要確認", "推定", "未入力", "（", "(")):
            issues.append(OutputValidationIssue("OUT-005", "main_query must contain only the query string"))

        if not changes.get("body", False) and package.get("body_additions"):
            issues.append(OutputValidationIssue("OUT-006", "body additions require changes.body=true"))

        if changes.get("internal_links", False):
            for link in package.get("internal_link_report", []):
                if link.get("classification") == "adopted" and not link.get("verified", False):
                    issues.append(OutputValidationIssue("OUT-007", "unverified internal links cannot be adopted"))

        if mode not in {"full", "publish"} and package.get("article_content"):
            issues.append(OutputValidationIssue("OUT-008", "article_content is allowed only in full or publish mode"))

        if mode == "json_only" and package.get("user_output"):
            issues.append(OutputValidationIssue("OUT-009", "json_only mode must not include user_output"))

        user_text = str(package.get("rendered_user_output") or "")
        if user_text and any(re.search(pattern, user_text) for pattern in FORBIDDEN_PREFACE_PATTERNS):
            issues.append(OutputValidationIssue("OUT-011", "user output must start with the artifact, without greetings or honorifics"))

        new_values = feedback.get("new_values") or {}
        seo_title = str(new_values.get("seo_title") or "")
        description = str(new_values.get("description") or new_values.get("meta_description") or "")
        if len(seo_title) > SEO_TITLE_HARD_MAX:
            issues.append(OutputValidationIssue("OUT-012", f"seo_title exceeds {SEO_TITLE_HARD_MAX} characters"))
        elif len(seo_title) > SEO_TITLE_RECOMMENDED_MAX:
            issues.append(OutputValidationIssue("OUT-013", f"seo_title exceeds recommended {SEO_TITLE_RECOMMENDED_MAX} characters", "warning"))
        if len(description) > META_DESCRIPTION_HARD_MAX:
            issues.append(OutputValidationIssue("OUT-014", f"description exceeds {META_DESCRIPTION_HARD_MAX} characters"))
        elif len(description) > META_DESCRIPTION_RECOMMENDED_MAX:
            issues.append(OutputValidationIssue("OUT-015", f"description exceeds recommended {META_DESCRIPTION_RECOMMENDED_MAX} characters", "warning"))

        rendered_response = str(package.get("rendered_response") or "")
        prose_output = str(package.get("rendered_user_output") or rendered_response)
        if re.search(r"<(?:div|pre|code)\b|\bstyle\s*=", prose_output, re.IGNORECASE):
            issues.append(OutputValidationIssue("OUT-032", "Before/After prose must not contain raw HTML wrappers"))
        if rendered_response:
            if not re.search(r"```json\s*\n\s*\{.*?\}\s*\n```\s*$", rendered_response, re.DOTALL):
                issues.append(OutputValidationIssue("OUT-016", "response must end with exactly one fenced ```json code block"))
            if len(re.findall(r"```json\b", rendered_response)) != 1:
                issues.append(OutputValidationIssue("OUT-017", "response must contain exactly one JSON code block"))

        if package.get("publish_quality"):
            for message in validate_before_after_editorial(package.get("user_output") or []):
                issues.append(OutputValidationIssue("OUT-023", message))

        if package.get("comparison_validation"):
            for message in validate_comparison_article(package.get("comparison_validation") or {}):
                issues.append(OutputValidationIssue("OUT-024", message))

        expected = feedback.get("expected_effect") or {}
        for key in ("ctr", "clicks"):
            value = str(expected.get(key, ""))
            numeric_prediction = bool(re.search(r"(?:\d+(?:\.\d+)?\s*%|[+＋]\s*\d+|\d+\s*[〜～-]\s*\d+\s*(?:%|クリック))", value))
            if numeric_prediction and not package.get("effect_evidence", {}).get(key):
                issues.append(OutputValidationIssue("OUT-010", f"numeric {key} prediction requires evidence"))

        return issues

    def assert_valid(self, package: dict[str, Any]) -> None:
        issues = self.validate(package)
        errors = [i for i in issues if i.severity == "error"]
        if errors:
            detail = "; ".join(f"{i.code}: {i.message}" for i in errors)
            raise ValueError(detail)


def infer_change_flags(before_after: list[dict[str, Any]], *, body_additions: list[dict[str, Any]] | None = None,
                       internal_link_report: list[dict[str, Any]] | None = None) -> dict[str, bool]:
    flags = {key: False for key in CHANGE_KEYS}
    mapping = {
        "article_title": "article_title", "seo_title": "seo_title", "description": "description",
        "introduction": "introduction", "heading": "headings", "headings": "headings",
        "faq": "faq", "body": "body", "image": "images", "images": "images",
    }
    for item in before_after:
        component = mapping.get(str(item.get("component", "")).lower())
        if component and item.get("before") != item.get("after"):
            flags[component] = True
    if body_additions:
        flags["body"] = True
    if any(x.get("classification") == "adopted" and x.get("applied") for x in (internal_link_report or [])):
        flags["internal_links"] = True
    return flags


def build_feedback(*, article_id: str | None, article_url: str | None, main_query: str,
                   site_id: str | None = None, site_name: str | None = None,
                   site_url: str | None = None,
                   before_after: list[dict[str, Any]], summary: str, warnings: list[str],
                   information: list[str] | None = None,
                   main_query_source: str = "manual",
                   execution_mode: str = "standard",
                   estimated_fields: list[str] | None = None,
                   body_additions: list[dict[str, Any]] | None = None,
                   internal_link_report: list[dict[str, Any]] | None = None,
                   confidence: str = "medium", improvement_type: str = "normal",
                   next_action: str = "remeasure", recommended_review_days: int = 14,
                   expected_effect: dict[str, str] | None = None) -> dict[str, Any]:
    changes = infer_change_flags(
        before_after,
        body_additions=body_additions,
        internal_link_report=internal_link_report,
    )
    new_values = {"article_title": "", "seo_title": "", "description": "", "main_query": main_query}
    for item in before_after:
        component = item.get("component")
        if component == "article_title": new_values["article_title"] = item.get("after", "")
        elif component == "seo_title": new_values["seo_title"] = item.get("after", "")
        elif component == "description": new_values["description"] = item.get("after", "")
    feedback = {
        "format": "SIMS_FEEDBACK_V2",
        "version": "2.0",
        "article_id": article_id or "",
        "article_url": article_url or "",
        "completed_at": date.today().isoformat(),
        "changes": changes,
        "new_values": new_values,
        "main_query_source": main_query_source,
        "execution_mode": execution_mode,
        "estimated_fields": list(estimated_fields or []),
        "improvement_type": improvement_type,
        "confidence": confidence,
        "expected_effect": expected_effect or {"ctr": "", "clicks": ""},
        "next_action": next_action,
        "summary": summary,
        "warnings": warnings,
        "information": list(information or []),
        "estimated_minutes": 20,
        "recommended_review_days": recommended_review_days,
    }
    # Product 5.3.1 identifiers are transparent optional fields. Writer does not generate,
    # repair, deduplicate, or audit them; absent legacy fields remain absent.
    identity = {"site_id": site_id, "site_name": site_name, "site_url": site_url}
    if any(value not in (None, "") for value in identity.values()):
        feedback = {
            "format": feedback.pop("format"),
            "version": feedback.pop("version"),
            **{key: value or "" for key, value in identity.items()},
            **feedback,
        }
    return feedback


def package_output(*, output_mode: str, before_after: list[dict[str, Any]], feedback: dict[str, Any],
                   internal_link_report: list[dict[str, Any]] | None = None,
                   unresolved_items: list[str] | None = None,
                   body_additions: list[dict[str, Any]] | None = None,
                   article_content: str | None = None,
                   effect_evidence: dict[str, Any] | None = None,
                   user_json_contract: dict[str, Any] | None = None,
                   publish_quality: dict[str, Any] | None = None) -> dict[str, Any]:
    if output_mode not in OUTPUT_MODES:
        raise ValueError(f"Unsupported output mode: {output_mode}")
    package = {
        "output_mode": output_mode,
        "user_output": [] if output_mode == "json_only" else deepcopy(before_after),
        "internal_link_report": deepcopy(internal_link_report or []),
        "unresolved_items": list(unresolved_items or []),
        "body_additions": deepcopy(body_additions or []),
        "feedback": deepcopy(feedback),
        "effect_evidence": deepcopy(effect_evidence or {}),
        "publish_quality": deepcopy(publish_quality or {}),
    }
    if user_json_contract is not None:
        package["user_json_contract"] = deepcopy(user_json_contract)
    if output_mode in {"full", "publish"}:
        package["article_content"] = article_content or ""
    OutputContractValidator().assert_valid(package)
    return package
