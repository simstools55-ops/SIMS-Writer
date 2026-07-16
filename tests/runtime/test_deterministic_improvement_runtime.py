from pathlib import Path
import json

from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator

ROOT = Path(__file__).resolve().parents[2]


def _request() -> dict:
    return {
        "request_id": "REQ-V040-001",
        "request_type": "existing_article_improvement",
        "language": "ja",
        "target_url": "https://example.com/wifi-cost",
        "current_title": "ルーターの費用について",
        "seo_title": "ルーターの費用について",
        "meta_description": "ルーターの費用を説明します。",
        "main_query": "wi-fi 電気代",
        "supporting_queries": ["wifi ルーター 電気代 つけっぱなし", "wifi7 電気代"],
        "improvement_goal": ["seo_title", "introduction", "faq"],
        "requested_output": ["before_after", "change_reason"],
        "existing_content": "<article><h1>ルーターの費用について</h1><p>Wi-Fiルーターは毎日使う機器です。消費電力から電気代を計算できます。</p></article>",
        "content_format": "html",
        "performance": {"clicks": 5, "impressions": 2773, "ctr": 0.002, "average_position": 10.0},
        "source_system": "generic_json",
        "schema_version": "1.0",
    }


def test_default_runtime_generates_grounded_improvement_package():
    result = RuntimeOrchestrator(ROOT).execute(_request())
    data = result.to_dict()
    draft = data["artifacts"]["content_draft"]
    package = data["artifacts"]["publication_package"]

    assert result.status in {"publish_ready", "publish_ready_with_advisory"}
    assert draft["draft_status"] == "generated"
    assert draft["adapter"] == "deterministic-ctr-improvement-adapter"
    assert "wi-fi" in draft["seo_title"].lower()
    assert len(draft["faq"]) == 2
    assert draft["before_after"]["seo_title"]["before"] == "ルーターの費用について"
    assert package["article_content"]
    assert data["artifacts"]["knowledge_assembly"]["selected"]
    assert data["artifacts"]["content_plan"]["status"] == "ready"


def test_runtime_requires_source_for_grounded_improvement():
    request = _request()
    request["existing_content"] = ""
    result = RuntimeOrchestrator(ROOT).execute(request)
    stages = {item.name: item.status for item in result.stages}
    assert stages["source_acquisition"] == "manual_review_required"
    assert stages["content_planning"] == "manual_review_required"
