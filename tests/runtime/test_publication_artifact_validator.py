from pathlib import Path
import json

from runtime.sims_writer_runtime.export import PublicationArtifactValidator


def _write_valid_set(root: Path) -> None:
    runtime = {"execution_id": "EXE-001", "request_id": "REQ-001", "status": "publish_ready"}
    package = {
        "publish_decision": "publish_ready",
        "article_content": "十分な長さの本文です。" * 20,
        "seo_title": "検証用SEOタイトル",
        "meta_description": "検証用メタディスクリプションです。",
        "h1": "検証用記事",
        "quality_summary": {"publish_recommendation": "publish_ready"},
    }
    manifest = {"execution_id": "EXE-001", "request_id": "REQ-001", "status": "publish_ready"}
    (root / "runtime-result.json").write_text(json.dumps(runtime, ensure_ascii=False), encoding="utf-8")
    (root / "publication-package.json").write_text(json.dumps(package, ensure_ascii=False), encoding="utf-8")
    (root / "execution-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    (root / "article.md").write_text("# 検証用記事\n\n" + "十分な長さの本文です。" * 20, encoding="utf-8")
    (root / "improvement-report.md").write_text("# 改善レポート\n\n検証内容です。", encoding="utf-8")


def test_validator_accepts_complete_consistent_artifacts(tmp_path):
    _write_valid_set(tmp_path)
    result = PublicationArtifactValidator().validate(tmp_path)
    assert result["artifact_status"] == "valid"
    assert result["release_ready"] is True
    assert result["summary"]["fail"] == 0
    assert set(result["checksums"]) == set(PublicationArtifactValidator.REQUIRED_FILES)


def test_validator_blocks_missing_or_inconsistent_artifacts(tmp_path):
    _write_valid_set(tmp_path)
    (tmp_path / "article.md").unlink()
    manifest = json.loads((tmp_path / "execution-manifest.json").read_text(encoding="utf-8"))
    manifest["execution_id"] = "EXE-DIFFERENT"
    (tmp_path / "execution-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    result = PublicationArtifactValidator().validate(tmp_path)
    assert result["artifact_status"] == "invalid"
    assert result["release_ready"] is False
    assert result["summary"]["fail"] >= 2
