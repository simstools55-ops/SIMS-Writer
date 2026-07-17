from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLAUDE = ROOT / "claude"


def test_required_claude_distribution_files_exist() -> None:
    required = [
        CLAUDE / "CLAUDE_PROJECT_INSTRUCTIONS.md",
        CLAUDE / "knowledge" / "SIMS_WRITER_KNOWLEDGE_PACK.md",
        CLAUDE / "templates" / "IMPROVEMENT_REQUEST_TEMPLATE.json",
        CLAUDE / "examples" / "EXAMPLE_REQUEST.json",
        CLAUDE / "SETUP_GUIDE.md",
        CLAUDE / "README.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    assert not missing, f"Missing Claude distribution files: {missing}"


def test_instruction_contract_contains_required_controls() -> None:
    text = (CLAUDE / "CLAUDE_PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")
    for token in [
        "manual_review_required",
        "unresolved_items",
        "internal_link_recommendations",
        "separate_article_candidates",
        "事実を創作しない",
    ]:
        assert token in text


def test_request_templates_are_valid_json_and_have_required_fields() -> None:
    required = {"request_id", "article_id", "target_url", "current_title", "main_query", "metrics", "existing_content"}
    for path in [
        CLAUDE / "templates" / "IMPROVEMENT_REQUEST_TEMPLATE.json",
        CLAUDE / "examples" / "EXAMPLE_REQUEST.json",
    ]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert required <= payload.keys()
        assert {"clicks", "impressions", "ctr", "position"} <= payload["metrics"].keys()


def test_distribution_is_small_and_curated() -> None:
    files = [path for path in CLAUDE.rglob("*") if path.is_file()]
    assert len(files) <= 10
    assert sum(path.stat().st_size for path in files) < 100_000
