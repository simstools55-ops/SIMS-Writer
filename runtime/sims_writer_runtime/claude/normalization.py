from __future__ import annotations

from copy import deepcopy
from typing import Any


class ClaudeOutputNormalizer:
    """Normalize limited, known Claude output variations without inventing content."""

    KEY_ALIASES = {
        "seoTitle": "seo_title",
        "metaDescription": "meta_description",
        "articleContent": "article_content",
        "changeSummary": "change_summary",
        "internalLinkRecommendations": "internal_link_recommendations",
        "separateArticleCandidates": "separate_article_candidates",
        "unresolvedItems": "unresolved_items",
    }
    STATUS_ALIASES = {
        "complete": "generated",
        "completed": "generated",
        "生成済み": "generated",
        "要確認": "manual_review_required",
        "manual-review-required": "manual_review_required",
    }
    ARRAY_FIELDS = (
        "change_summary",
        "faq",
        "internal_link_recommendations",
        "separate_article_candidates",
        "unresolved_items",
    )

    @classmethod
    def normalize(cls, payload: Any) -> tuple[Any, list[str]]:
        if not isinstance(payload, dict):
            return payload, []
        normalized = deepcopy(payload)
        warnings: list[str] = []

        for alias, canonical in cls.KEY_ALIASES.items():
            if alias in normalized and canonical not in normalized:
                normalized[canonical] = normalized.pop(alias)
                warnings.append(f"normalized:key_alias:{alias}->{canonical}")

        status = normalized.get("status")
        if isinstance(status, str):
            stripped = status.strip()
            mapped = cls.STATUS_ALIASES.get(stripped, stripped)
            if mapped != status:
                warnings.append(f"normalized:status:{status}->{mapped}")
            normalized["status"] = mapped

        for key in ("seo_title", "meta_description", "h1", "article_content"):
            value = normalized.get(key)
            if isinstance(value, str):
                trimmed = value.strip()
                if trimmed != value:
                    warnings.append(f"normalized:trimmed:{key}")
                normalized[key] = trimmed or None

        for key in cls.ARRAY_FIELDS:
            if key not in normalized or normalized[key] is None:
                normalized[key] = []
                warnings.append(f"normalized:default_empty_array:{key}")

        for key in cls.ARRAY_FIELDS:
            value = normalized.get(key)
            if isinstance(value, list):
                cls._trim_list_items(value, key, warnings)

        return normalized, warnings

    @staticmethod
    def _trim_list_items(items: list[Any], field: str, warnings: list[str]) -> None:
        for index, item in enumerate(items):
            if isinstance(item, str):
                trimmed = item.strip()
                if trimmed != item:
                    items[index] = trimmed
                    warnings.append(f"normalized:trimmed:{field}[{index}]")
            elif isinstance(item, dict):
                for key, value in list(item.items()):
                    if isinstance(value, str):
                        trimmed = value.strip()
                        if trimmed != value:
                            item[key] = trimmed
                            warnings.append(f"normalized:trimmed:{field}[{index}].{key}")
