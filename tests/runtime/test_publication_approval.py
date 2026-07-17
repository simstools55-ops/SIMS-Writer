from pathlib import Path
import json
import pytest

from runtime.sims_writer_runtime.export import (
    PublicationApprovalError,
    PublicationApprovalManager,
    ResultArtifactWriter,
)
from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator

ROOT = Path(__file__).resolve().parents[2]


def _request() -> dict:
    return {
        "request_id": "REQ-V090-001",
        "request_type": "existing_article_improvement",
        "language": "ja",
        "target_url": "https://example.com/approval",
        "current_title": "DiscordをiPhoneで翻訳する方法",
        "seo_title": "DiscordをiPhoneで翻訳する方法",
        "meta_description": "Discordの翻訳方法を紹介します。",
        "main_query": "discord 翻訳 iphone",
        "supporting_queries": ["discord 自動翻訳 iphone", "discord 翻訳 できない"],
        "improvement_goal": ["seo_title", "introduction", "faq"],
        "requested_output": ["before_after", "change_reason"],
        "existing_content": "<article><h1>DiscordをiPhoneで翻訳する方法</h1><p>本文です。</p></article>",
        "content_format": "html",
        "performance": {"clicks": 20, "impressions": 1200, "ctr": 0.016, "average_position": 7.0},
        "source_system": "generic_json",
        "schema_version": "1.0",
    }


def _generate(tmp_path):
    result = RuntimeOrchestrator(ROOT).execute(_request())
    ResultArtifactWriter().write(result, tmp_path)
    return result


def test_writer_initializes_pending_review(tmp_path):
    result = _generate(tmp_path)
    approval = json.loads((tmp_path / "publication-approval.json").read_text(encoding="utf-8"))
    history = json.loads((tmp_path / "approval-history.json").read_text(encoding="utf-8"))
    assert approval["execution_id"] == result.execution_id
    assert approval["status"] == "pending_review"
    assert history["event_count"] == 1
    assert history["events"][0]["action"] == "pending_review"


def test_approve_and_finalize_create_immutable_release_snapshot(tmp_path):
    result = _generate(tmp_path)
    manager = PublicationApprovalManager()
    approved = manager.approve(tmp_path, "幹事長", "内容を確認済み")
    manifest = manager.finalize(tmp_path, "幹事長")

    release_dir = tmp_path / "release" / result.execution_id
    approval = json.loads((tmp_path / "publication-approval.json").read_text(encoding="utf-8"))
    history = json.loads((tmp_path / "approval-history.json").read_text(encoding="utf-8"))

    assert approved["status"] == "approved"
    assert manifest["status"] == "finalized"
    assert manifest["release_ready"] is True
    assert approval["status"] == "finalized"
    assert (release_dir / "article.md").is_file()
    assert (release_dir / "finalization-manifest.json").is_file()
    assert len(manifest["checksums"]) == len(PublicationApprovalManager.FINALIZED_FILES)
    assert [event["action"] for event in history["events"]] == ["pending_review", "approved", "finalized"]


def test_rejected_artifacts_cannot_be_finalized(tmp_path):
    _generate(tmp_path)
    manager = PublicationApprovalManager()
    rejected = manager.reject(tmp_path, "reviewer", "FAQの根拠を再確認する")
    assert rejected["status"] == "rejected"
    with pytest.raises(PublicationApprovalError, match="approved before finalization"):
        manager.finalize(tmp_path)


def test_approval_rejects_non_release_ready_artifacts(tmp_path):
    _generate(tmp_path)
    validation_path = tmp_path / "artifact-validation.json"
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    validation["release_ready"] = False
    validation_path.write_text(json.dumps(validation, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(PublicationApprovalError, match="release-ready"):
        PublicationApprovalManager().approve(tmp_path, "reviewer")
