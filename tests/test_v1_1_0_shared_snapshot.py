from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared"


def test_shared_snapshot_metadata():
    assert (SHARED / "VERSION").read_text(encoding="utf-8").strip() == "1.0.0"
    source = (SHARED / "SOURCE.md").read_text(encoding="utf-8")
    assert "SIMS-Shared-Editorial-Knowledge" in source
    assert "SIMS Writer 1.1.0-rc2" in source


def test_shared_snapshot_required_assets():
    required = [
        "knowledge/intent-analysis.md",
        "knowledge/hidden-anxiety.md",
        "knowledge/evidence-transparency.md",
        "knowledge/serp-entity-preservation.md",
        "knowledge/internal-link-semantics.md",
        "knowledge/decision-support.md",
        "knowledge/freshness-safety.md",
        "mappings/writer/application-mapping.md",
        "validation/shared-knowledge-validation.md",
        "docs/integration-policy.md",
        "docs/scope.md",
    ]
    for rel in required:
        assert (SHARED / rel).is_file(), rel


def test_shared_snapshot_manifest_hashes():
    manifest = json.loads((SHARED / "SNAPSHOT_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["source_repository"] == "SIMS-Shared-Editorial-Knowledge"
    assert manifest["source_version"] == "1.0.0"
    assert manifest["integrated_version"] == "1.1.0-rc2"
    for item in manifest["files"]:
        path = SHARED / item["path"]
        assert path.is_file(), item["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
