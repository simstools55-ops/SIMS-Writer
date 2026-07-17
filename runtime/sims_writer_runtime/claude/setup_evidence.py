from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


class BeginnerSetupEvidenceError(ValueError):
    pass


@dataclass(frozen=True)
class BeginnerSetupValidation:
    valid: bool
    completed: bool
    operator_level: str
    passed_steps: int
    total_steps: int
    blockers: list[str]
    errors: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class BeginnerSetupEvidenceValidator:
    """Validate measured beginner setup evidence without inferring success."""

    required_steps = (
        "create_claude_project",
        "set_project_instructions",
        "upload_knowledge_files",
        "submit_example_request",
        "save_json_output",
    )

    def validate_file(self, path: Path) -> BeginnerSetupValidation:
        path = path.resolve()
        if not path.is_file():
            raise BeginnerSetupEvidenceError(f"beginner setup evidence not found: {path}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise BeginnerSetupEvidenceError(f"invalid beginner setup evidence: {exc}") from exc

        errors: list[str] = []
        operator_level = str(data.get("operator_level", "")).strip()
        completed = data.get("completed")
        if operator_level != "beginner":
            errors.append("operator_level must be beginner")
        if not isinstance(completed, bool):
            errors.append("completed must be boolean")
            completed = False
        steps = data.get("steps")
        if not isinstance(steps, list):
            errors.append("steps must be an array")
            steps = []
        step_map: dict[str, dict[str, Any]] = {}
        for item in steps:
            if not isinstance(item, dict) or not str(item.get("step_id", "")).strip():
                errors.append("each step must include step_id")
                continue
            step_id = str(item["step_id"]).strip()
            if step_id in step_map:
                errors.append(f"duplicate step_id: {step_id}")
            step_map[step_id] = item
        for step_id in self.required_steps:
            item = step_map.get(step_id)
            if item is None:
                errors.append(f"missing required step: {step_id}")
            elif item.get("status") != "passed":
                errors.append(f"required step not passed: {step_id}")
        blockers_raw = data.get("blockers", [])
        if not isinstance(blockers_raw, list) or any(not isinstance(x, str) or not x.strip() for x in blockers_raw):
            errors.append("blockers must be an array of non-empty strings")
            blockers: list[str] = []
        else:
            blockers = [x.strip() for x in blockers_raw]
        if completed is True and blockers:
            errors.append("completed setup cannot have open blockers")
        if completed is True and errors:
            completed = False
        passed_steps = sum(1 for step_id in self.required_steps if step_map.get(step_id, {}).get("status") == "passed")
        return BeginnerSetupValidation(
            valid=not errors,
            completed=bool(completed) and not errors,
            operator_level=operator_level,
            passed_steps=passed_steps,
            total_steps=len(self.required_steps),
            blockers=blockers,
            errors=errors,
        )
