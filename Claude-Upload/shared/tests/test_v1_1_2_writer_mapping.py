from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def test_writer_mapping_boundary():
    text=(ROOT/"mappings/writer/application-mapping.md").read_text(encoding="utf-8")
    assert "v1.2.0 Platform and Quality application boundary" in text
    assert "SIMS_PLATFORM_GUIDE.md" in text
    assert "QUALITY_FRAMEWORK.md" in text

def test_version():
    assert (ROOT/"VERSION").read_text().strip()=="3.5.0"
