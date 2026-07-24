from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DOCS = [
    Path("product/platform/SIMS_PLATFORM_GUIDE.md"),
    Path("product/quality/QUALITY_FRAMEWORK.md"),
    Path("product/roadmap/WRITER_v1.1.2_IMPROVEMENT_PLAN.md"),
]

def test_sprint1_documents_exist_and_versioned():
    for rel in DOCS:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "Version: 1.2.0" in text
        assert len(text) > 1000

def test_claude_product_guides_are_exact_copies():
    for rel in DOCS:
        assert (ROOT / rel).read_bytes() == (ROOT / "claude" / rel).read_bytes()

def test_shared_mapping_keeps_product_boundary():
    text = (ROOT / "shared/mappings/writer/application-mapping.md").read_text(encoding="utf-8")
    assert "v1.2.0 Platform and Quality application boundary" in text
    assert "not promoted to Shared Knowledge" in text

def test_release_versions_are_synchronized():
    assert (ROOT / "VERSION").read_text().strip() == "1.3.0"
    assert (ROOT / "claude/VERSION").read_text().strip() == "1.3.0"
    assert (ROOT / "shared/VERSION").read_text().strip() == "1.3.0"
