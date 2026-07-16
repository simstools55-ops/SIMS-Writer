from pathlib import Path
import json

from runtime.sims_writer_runtime.export import ResultArtifactWriter
from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator

ROOT = Path(__file__).resolve().parents[2]


def _request(title: str = "DiscordをiPhoneで翻訳する方法") -> dict:
    return {
        "request_id": "REQ-V070-001",
        "request_type": "existing_article_improvement",
        "language": "ja",
        "target_url": "https://example.com/discord-translation",
        "current_title": title,
        "seo_title": title,
        "meta_description": "Discordの翻訳方法を紹介します。",
        "main_query": "discord 翻訳 iphone",
        "supporting_queries": ["discord 自動翻訳 iphone"],
        "improvement_goal": ["seo_title", "introduction", "faq"],
        "requested_output": ["before_after", "change_reason"],
        "existing_content": f"<article><h1>{title}</h1><p>標準機能と翻訳アプリを使う方法があります。</p></article>",
        "content_format": "html",
        "performance": {"clicks": 20, "impressions": 1200, "ctr": 0.016, "average_position": 7.0},
        "source_system": "generic_json",
        "schema_version": "1.0",
    }


def test_first_execution_creates_baseline_history(tmp_path):
    result = RuntimeOrchestrator(ROOT).execute(_request())
    ResultArtifactWriter().write(result, tmp_path)
    diff = json.loads((tmp_path / "artifact-diff.json").read_text(encoding="utf-8"))
    history = json.loads((tmp_path / "execution-history.json").read_text(encoding="utf-8"))
    assert diff["baseline"] == "initial_execution"
    assert diff["changed"] is False
    assert history["execution_count"] == 1
    assert history["latest_execution_id"] == result.execution_id


def test_second_execution_archives_previous_and_reports_changes(tmp_path):
    writer = ResultArtifactWriter()
    first = RuntimeOrchestrator(ROOT).execute(_request())
    writer.write(first, tmp_path)
    second = RuntimeOrchestrator(ROOT).execute(_request("Discord翻訳をiPhoneで使う方法"))
    writer.write(second, tmp_path)

    archive = tmp_path / ".history" / first.execution_id
    assert (archive / "runtime-result.json").is_file()
    assert (archive / "article.md").is_file()
    diff = json.loads((tmp_path / "artifact-diff.json").read_text(encoding="utf-8"))
    history = json.loads((tmp_path / "execution-history.json").read_text(encoding="utf-8"))
    assert diff["previous_execution_id"] == first.execution_id
    assert diff["current_execution_id"] == second.execution_id
    assert diff["changed"] is True
    assert "publication-package.json" in diff["changed_files"]
    assert history["execution_count"] == 2
    assert history["executions"][0]["superseded"] is True
