from pathlib import Path

from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator
from runtime.sims_writer_runtime.search_intent import SearchIntentAnalyzer

ROOT = Path(__file__).resolve().parents[2]


def test_analyzer_clusters_cost_and_troubleshooting_queries():
    result = SearchIntentAnalyzer().analyze(
        "wi-fi 電気代",
        ["wifi ルーター 電気代 つけっぱなし", "wifi7 電気代", "wifi 電気代 高い 原因"],
    )
    assert result["primary"]["intent"] == "cost"
    assert result["query_count"] == 4
    assert "cost" in result["intent_clusters"]
    assert "troubleshooting" in result["intent_clusters"]
    assert result["analysis_basis"] == "supplied_queries_only"
    assert len(result["faq_candidates"]) == 3


def test_runtime_uses_search_intent_in_plan_and_draft():
    request = {
        "request_id": "REQ-V140-001",
        "request_type": "existing_article_improvement",
        "language": "ja",
        "target_url": "https://example.com/discord-translate",
        "current_title": "Discordを便利に使う",
        "seo_title": "Discordを便利に使う",
        "meta_description": "Discordの使い方を紹介します。",
        "main_query": "discord 翻訳 iphone",
        "supporting_queries": ["discord 翻訳 iphone できない", "discord 自動翻訳 設定"],
        "improvement_goal": ["seo_title", "introduction", "headings", "faq"],
        "requested_output": ["before_after", "change_reason"],
        "existing_content": "<article><h1>Discordを便利に使う</h1><p>Discordにはさまざまな機能があります。iPhoneでも利用できます。</p></article>",
        "content_format": "html",
        "performance": {"clicks": 12, "impressions": 1800, "ctr": 0.006, "average_position": 8.0},
        "source_system": "generic_json",
        "schema_version": "1.0",
    }
    result = RuntimeOrchestrator(ROOT).execute(request)
    artifacts = result.artifacts
    analysis = artifacts["search_intent_analysis"]
    plan = artifacts["content_plan"]
    draft = artifacts["content_draft"]

    assert analysis["primary"]["intent"] == "how_to"
    assert plan["primary_intent"] == "how_to"
    assert plan["recommended_headings"]
    assert draft["recommended_headings"] == plan["recommended_headings"]
    assert len(draft["faq"]) == 2
    assert "できない" in draft["faq"][0]["question"]
