from pathlib import Path

from runtime.sims_writer_runtime.link_analysis import LinkOpportunityAnalyzer
from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator

ROOT = Path(__file__).resolve().parents[2]


def test_selects_internal_links_and_separates_low_relevance_queries():
    result = LinkOpportunityAnalyzer().analyze(
        "discord 翻訳 iphone",
        ["discord 自動翻訳 設定", "discord 翻訳 できない", "windows11 スクリーンショット 保存先"],
        [
            {"article_id":"A2", "url":"https://example.com/discord-setting", "title":"Discordの自動翻訳設定", "main_query":"discord 自動翻訳 設定"},
            {"article_id":"A3", "url":"https://example.com/windows-shot", "title":"Windows11のスクリーンショット保存先", "main_query":"windows11 スクリーンショット 保存先"},
        ],
        current_url="https://example.com/current",
    )
    assert result["candidate_count"] == 1
    assert result["internal_link_candidates"][0]["article_id"] == "A2"
    assert result["separate_article_queries"][0]["query"].startswith("windows11")


def test_runtime_exposes_link_analysis_in_plan_and_draft():
    request = {
        "schema_version":"1.0", "request_id":"REQ-V150-001", "request_type":"existing_article_improvement",
        "language":"ja", "target_url":"https://example.com/current", "current_title":"Discord翻訳",
        "main_query":"discord 翻訳 iphone",
        "supporting_queries":["discord 自動翻訳 設定", "windows11 スクリーンショット 保存先"],
        "improvement_goal":["seo_title","internal_links"], "requested_output":["publication_package"],
        "existing_content":"<article><h1>Discord翻訳</h1><p>iPhoneで翻訳する方法を説明します。</p></article>",
        "content_format":"html", "source_system":"generic_json",
        "article_catalog":[
            {"article_id":"A2", "url":"https://example.com/discord-setting", "title":"Discord自動翻訳の設定", "main_query":"discord 自動翻訳 設定"}
        ]
    }
    result = RuntimeOrchestrator(ROOT).execute(request)
    analysis = result.artifacts["link_opportunity_analysis"]
    assert analysis["candidate_count"] == 1
    assert result.artifacts["content_plan"]["internal_link_candidates"]
    assert result.artifacts["content_draft"]["internal_link_recommendations"]
    assert result.artifacts["content_draft"]["separate_article_queries"]
