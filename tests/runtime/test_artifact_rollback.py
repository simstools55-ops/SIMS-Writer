from pathlib import Path
import json
import pytest

from runtime.sims_writer_runtime.export import ArtifactRollbackError, ArtifactRollbackManager, ResultArtifactWriter
from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator

ROOT = Path(__file__).resolve().parents[2]


def _request(title: str) -> dict:
    return {
        "request_id": "REQ-V080-001",
        "request_type": "existing_article_improvement",
        "language": "ja",
        "target_url": "https://example.com/rollback",
        "current_title": title,
        "seo_title": title,
        "meta_description": "ロールバック検証用の記事です。",
        "main_query": "discord 翻訳 iphone",
        "supporting_queries": ["discord 自動翻訳 iphone"],
        "improvement_goal": ["seo_title", "introduction", "faq"],
        "requested_output": ["before_after", "change_reason"],
        "existing_content": f"<article><h1>{title}</h1><p>本文です。</p></article>",
        "content_format": "html",
        "performance": {"clicks": 20, "impressions": 1200, "ctr": 0.016, "average_position": 7.0},
        "source_system": "generic_json",
        "schema_version": "1.0",
    }


def test_rollback_restores_previous_artifacts_and_records_manifest(tmp_path):
    writer = ResultArtifactWriter()
    first = RuntimeOrchestrator(ROOT).execute(_request("最初の記事タイトル"))
    writer.write(first, tmp_path)
    first_article = (tmp_path / "article.md").read_text(encoding="utf-8")

    second = RuntimeOrchestrator(ROOT).execute(_request("更新後の記事タイトル"))
    writer.write(second, tmp_path)
    assert (tmp_path / "article.md").read_text(encoding="utf-8") != first_article

    manifest = ArtifactRollbackManager().rollback(tmp_path, first.execution_id)
    restored = json.loads((tmp_path / "runtime-result.json").read_text(encoding="utf-8"))
    history = json.loads((tmp_path / "execution-history.json").read_text(encoding="utf-8"))

    assert restored["execution_id"] == first.execution_id
    assert (tmp_path / "article.md").read_text(encoding="utf-8") == first_article
    assert manifest["rolled_back_from_execution_id"] == second.execution_id
    assert manifest["release_ready"] is True
    assert history["latest_execution_id"] == first.execution_id
    assert history["last_operation"] == "rollback"
    assert (tmp_path / ".history" / second.execution_id / "runtime-result.json").is_file()
    assert (tmp_path / "rollback-manifest.json").is_file()


def test_rollback_rejects_unknown_execution(tmp_path):
    with pytest.raises(ArtifactRollbackError, match="execution-history"):
        ArtifactRollbackManager().rollback(tmp_path, "EX-NOT-FOUND")
