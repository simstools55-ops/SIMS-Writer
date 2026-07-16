from dataclasses import dataclass, field, asdict
from typing import Any

STAGES = [
    "intake", "normalization", "source_acquisition", "knowledge_assembly",
    "content_planning", "decision_evaluation", "pattern_selection",
    "content_production", "quality_validation", "refinement",
    "publication_packaging",
]

@dataclass
class StageRecord:
    name: str
    status: str = "pending"
    warnings: list[str] = field(default_factory=list)
    error: dict[str, Any] | None = None

@dataclass
class RuntimeResult:
    execution_id: str
    request_id: str
    status: str
    stages: list[StageRecord]
    manifest: dict[str, Any]
    artifacts: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d
