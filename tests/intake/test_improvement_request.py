from pathlib import Path
import json

import pytest

from runtime.sims_writer_runtime.article_context import ArticleContextBuilder
from runtime.sims_writer_runtime.intake.request_loader import ImprovementRequestLoader, RequestValidationError
from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator

ROOT = Path(__file__).resolve().parents[2]


def test_load_sbm_file_and_build_context():
    loader = ImprovementRequestLoader(ROOT)
    loaded = loader.load(ROOT / "examples/intake/sbm-improvement-request.json")
    assert loaded.input_type == "sbm"
    assert loaded.schema_version == "1.0"
    assert loaded.payload["request_id"] == "REQ-SBM-0001"
    context = ArticleContextBuilder.build(loaded.payload)
    assert context.article_id == "A000301"
    assert context.target_url == "https://example.com/entry/2025/12/28/043000"
    assert context.performance.ctr == pytest.approx(0.002)
    assert context.performance.impressions == 2773.0


def test_generic_request_is_detected_and_normalized():
    raw = {
        "request_id": "REQ-GEN-1",
        "article_id": "A1",
        "target_url": "https://EXAMPLE.com/test#top",
        "main_query": "  test query  ",
        "improvement_goal": ["ctr_improvement", "ctr_improvement"],
        "requested_output": ["publication_package"],
        "supporting_queries": [" sub ", "sub"],
        "performance": {"ctr": 2.5}
    }
    loaded = ImprovementRequestLoader(ROOT).load(raw)
    context = ArticleContextBuilder.build(loaded.payload)
    assert loaded.input_type == "generic"
    assert context.main_query == "test query"
    assert context.target_url == "https://example.com/test"
    assert context.supporting_queries == ["sub"]
    assert context.performance.ctr == pytest.approx(0.025)


def test_invalid_request_fails_explicitly():
    with pytest.raises(RequestValidationError, match="main_query"):
        ImprovementRequestLoader(ROOT).load({
            "request_id": "REQ-BAD",
            "improvement_goal": ["ctr_improvement"],
            "requested_output": ["publication_package"]
        }, input_type="generic")


def test_runtime_contains_article_context():
    raw = json.loads((ROOT / "examples/intake/sbm-improvement-request.json").read_text(encoding="utf-8"))
    result = RuntimeOrchestrator(ROOT).execute(raw)
    assert result.status != "failed"
    assert result.artifacts["request_metadata"]["input_type"] == "sbm"
    assert result.artifacts["article_context"]["article_id"] == "A000301"
