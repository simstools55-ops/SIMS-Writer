from __future__ import annotations

import json
from pathlib import Path

from runtime.sims_writer_runtime.claude.readiness import ClaudeUserTestReadinessEvaluator, write_readiness_report


def evidence(article: str, *, outcome: str = "generated", score: int = 5, beginner: bool = False, blockers=None):
    return {
        "evidence_id": f"UAT-{article}",
        "article_id": article,
        "request_id": f"REQ-{article}",
        "outcome": outcome,
        "scores": {
            "japanese_quality": score,
            "factual_grounding": score,
            "source_preservation": score,
            "internal_links": score,
            "output_completeness": score,
            "beginner_usability": score,
        },
        "blockers": blockers or [],
        "unresolved_items": ["本文不足"] if outcome == "manual_review_required" else [],
        "setup": {"operator_level": "beginner" if beginner else "developer", "completed": True, "notes": ""},
        "review_notes": "",
    }


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_readiness_passes_only_with_real_evidence_conditions(tmp_path: Path) -> None:
    write(tmp_path / "a.json", evidence("A001", beginner=True))
    write(tmp_path / "b.json", evidence("A002"))
    write(tmp_path / "c.json", evidence("A003"))
    write(tmp_path / "review.json", evidence("A004", outcome="manual_review_required"))
    report = ClaudeUserTestReadinessEvaluator().evaluate_directory(tmp_path)
    assert report["ready"] is True
    assert report["status"] == "user_test_ready"


def test_readiness_rejects_insufficient_or_low_quality_evidence(tmp_path: Path) -> None:
    write(tmp_path / "a.json", evidence("A001", score=3, beginner=True))
    write(tmp_path / "review.json", evidence("A002", outcome="manual_review_required"))
    report = ClaudeUserTestReadinessEvaluator().evaluate_directory(tmp_path)
    assert report["ready"] is False
    assert report["conditions"]["minimum_distinct_articles"] is False
    assert report["conditions"]["generated_quality_threshold"] is False


def test_readiness_rejects_open_blocker_and_missing_beginner_setup(tmp_path: Path) -> None:
    write(tmp_path / "a.json", evidence("A001", blockers=["タイトルが不自然"] ))
    write(tmp_path / "b.json", evidence("A002"))
    write(tmp_path / "c.json", evidence("A003"))
    write(tmp_path / "review.json", evidence("A004", outcome="manual_review_required"))
    report = ClaudeUserTestReadinessEvaluator().evaluate_directory(tmp_path)
    assert report["ready"] is False
    assert report["conditions"]["no_open_blockers"] is False
    assert report["conditions"]["beginner_setup_verified"] is False


def test_invalid_evidence_is_reported_and_report_files_are_written(tmp_path: Path) -> None:
    (tmp_path / "bad.json").write_text("{}", encoding="utf-8")
    report = ClaudeUserTestReadinessEvaluator().evaluate_directory(tmp_path)
    assert report["counts"]["invalid"] == 1
    out = tmp_path / "out"
    json_path, md_path = write_readiness_report(report, out)
    assert json_path.is_file()
    assert "not_user_test_ready" in md_path.read_text(encoding="utf-8")
