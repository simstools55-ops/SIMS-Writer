from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class QAReviewPolicy:
    """Writer/Creatorから独立して再利用できる公開前QA実行契約。"""

    max_review_cycles: int = 2
    allow_auto_fix: bool = True
    protected_fields: tuple[str, ...] = ()
    allowed_auto_fix_classes: tuple[str, ...] = (
        "placeholder_elimination",
        "ai_phrase_reduction",
        "redundancy_reduction",
        "heading_hierarchy_repair",
    )

    @classmethod
    def from_context(cls, context: dict[str, Any] | None) -> "QAReviewPolicy":
        data = (context or {}).get("qa_policy") or {}
        return cls(
            max_review_cycles=max(1, min(int(data.get("max_review_cycles", 2)), 3)),
            allow_auto_fix=bool(data.get("allow_auto_fix", True)),
            protected_fields=tuple(data.get("protected_fields") or ()),
            allowed_auto_fix_classes=tuple(data.get("allowed_auto_fix_classes") or cls().allowed_auto_fix_classes),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class QAReviewCycle:
    cycle: int
    verdict_before: str
    verdict_after: str
    auto_fix_applied: bool
    changed_fields: list[str] = field(default_factory=list)
    blocked_changes: list[str] = field(default_factory=list)
    revision_records: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
