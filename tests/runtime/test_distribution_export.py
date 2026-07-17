from pathlib import Path
import hashlib
import json
import zipfile
import pytest

from runtime.sims_writer_runtime.export import (
    DistributionExportError,
    DistributionPackageExporter,
    PublicationApprovalManager,
    ResultArtifactWriter,
)
from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator

ROOT = Path(__file__).resolve().parents[2]


def _request() -> dict:
    return {
        "request_id": "REQ-V100-001", "request_type": "existing_article_improvement", "language": "ja",
        "target_url": "https://example.com/export", "current_title": "DiscordをiPhoneで翻訳する方法",
        "seo_title": "DiscordをiPhoneで翻訳する方法", "meta_description": "Discordの翻訳方法を紹介します。",
        "main_query": "discord 翻訳 iphone", "supporting_queries": ["discord 自動翻訳 iphone"],
        "improvement_goal": ["seo_title", "introduction", "faq"], "requested_output": ["before_after"],
        "existing_content": "<article><h1>DiscordをiPhoneで翻訳する方法</h1><p>本文です。</p></article>",
        "content_format": "html", "performance": {"clicks": 20, "impressions": 1200, "ctr": 0.016, "average_position": 7.0},
        "source_system": "generic_json", "schema_version": "1.0",
    }


def _finalized(tmp_path: Path):
    result = RuntimeOrchestrator(ROOT).execute(_request())
    ResultArtifactWriter().write(result, tmp_path)
    manager = PublicationApprovalManager()
    manager.approve(tmp_path, "幹事長", "確認済み")
    manager.finalize(tmp_path, "幹事長")
    return result


def test_export_creates_verified_distribution_zip(tmp_path):
    result = _finalized(tmp_path)
    manifest = DistributionPackageExporter().export(tmp_path)
    archive_path = Path(manifest["archive_path"])
    assert manifest["status"] == "exported"
    assert manifest["execution_id"] == result.execution_id
    assert archive_path.is_file()
    assert hashlib.sha256(archive_path.read_bytes()).hexdigest() == manifest["archive_sha256"]
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        assert "distribution-manifest.json" in archive.namelist()
        assert "publication/article.md" in archive.namelist()
    saved = json.loads((tmp_path / "distribution" / "distribution-manifest.json").read_text(encoding="utf-8"))
    assert saved["archive_sha256"] == manifest["archive_sha256"]


def test_export_rejects_unfinalized_artifacts(tmp_path):
    result = RuntimeOrchestrator(ROOT).execute(_request())
    ResultArtifactWriter().write(result, tmp_path)
    with pytest.raises(DistributionExportError, match="finalization manifest"):
        DistributionPackageExporter().export(tmp_path)


def test_export_rejects_tampered_finalized_artifact(tmp_path):
    result = _finalized(tmp_path)
    release_article = tmp_path / "release" / result.execution_id / "article.md"
    release_article.write_text("tampered", encoding="utf-8")
    with pytest.raises(DistributionExportError, match="checksum mismatch"):
        DistributionPackageExporter().export(tmp_path)
