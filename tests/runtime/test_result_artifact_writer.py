from pathlib import Path
import json

from runtime.sims_writer_runtime.export import ResultArtifactWriter
from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator

ROOT = Path(__file__).resolve().parents[2]


def _request() -> dict:
    return {
        "request_id": "REQ-V050-001",
        "request_type": "existing_article_improvement",
        "language": "ja",
        "target_url": "https://example.com/discord-translation",
        "current_title": "DiscordをiPhoneで翻訳する方法",
        "seo_title": "DiscordをiPhoneで翻訳する方法",
        "meta_description": "Discordの翻訳方法を紹介します。",
        "main_query": "discord 翻訳 iphone",
        "supporting_queries": ["discord 自動翻訳 iphone", "discord 翻訳 できない"],
        "improvement_goal": ["seo_title", "introduction", "faq"],
        "requested_output": ["before_after", "change_reason"],
        "existing_content": "<article><h1>DiscordをiPhoneで翻訳する方法</h1><p>標準機能と翻訳アプリを使う方法があります。</p></article>",
        "content_format": "html",
        "performance": {"clicks": 20, "impressions": 1200, "ctr": 0.016, "average_position": 7.0},
        "source_system": "generic_json",
        "schema_version": "1.0",
    }


def test_writer_creates_complete_reviewable_artifact_set(tmp_path):
    result = RuntimeOrchestrator(ROOT).execute(_request())
    written = ResultArtifactWriter().write(result, tmp_path)

    expected = {
        "runtime-result.json", "publication-package.json", "article.md",
        "improvement-report.md", "execution-manifest.json",
    }
    assert {Path(path).name for path in written.values()} == expected
    assert all((tmp_path / name).exists() for name in expected)

    article = (tmp_path / "article.md").read_text(encoding="utf-8")
    report = (tmp_path / "improvement-report.md").read_text(encoding="utf-8")
    manifest = json.loads((tmp_path / "execution-manifest.json").read_text(encoding="utf-8"))
    package = json.loads((tmp_path / "publication-package.json").read_text(encoding="utf-8"))

    assert article.startswith("# ")
    assert "よくある質問" in article
    assert "Before / After" in report
    assert manifest["execution_id"] == result.execution_id
    assert package["seo_title"]


def test_writer_is_utf8_and_overwrites_same_output_safely(tmp_path):
    result = RuntimeOrchestrator(ROOT).execute(_request())
    writer = ResultArtifactWriter()
    writer.write(result, tmp_path)
    writer.write(result, tmp_path)
    assert "Discord" in (tmp_path / "article.md").read_text(encoding="utf-8")
