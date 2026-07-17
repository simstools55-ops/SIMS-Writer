from __future__ import annotations

import json
from pathlib import Path

from runtime.sims_writer_runtime.claude.setup_evidence import BeginnerSetupEvidenceValidator


def payload(completed=True):
    status = "passed" if completed else "pending"
    return {
        "operator_level": "beginner",
        "completed": completed,
        "steps": [
            {"step_id": step, "status": status, "notes": ""}
            for step in BeginnerSetupEvidenceValidator.required_steps
        ],
        "blockers": [],
    }


def test_beginner_setup_passes_only_when_all_measured_steps_pass(tmp_path: Path):
    path = tmp_path / "setup.json"
    path.write_text(json.dumps(payload()), encoding="utf-8")
    result = BeginnerSetupEvidenceValidator().validate_file(path)
    assert result.valid is True
    assert result.completed is True
    assert result.passed_steps == result.total_steps


def test_beginner_setup_rejects_missing_step(tmp_path: Path):
    data = payload()
    data["steps"] = data["steps"][:-1]
    path = tmp_path / "setup.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    result = BeginnerSetupEvidenceValidator().validate_file(path)
    assert result.valid is False
    assert any("missing required step" in error for error in result.errors)


def test_beginner_setup_rejects_completed_with_blocker(tmp_path: Path):
    data = payload()
    data["blockers"] = ["Knowledge upload failed"]
    path = tmp_path / "setup.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    result = BeginnerSetupEvidenceValidator().validate_file(path)
    assert result.valid is False
    assert result.completed is False
