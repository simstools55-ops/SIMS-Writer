from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
 "central-claim-evidence-priority.md", "source-scope-qualification.md",
 "evidence-strength-wording.md", "graceful-degradation.md",
 "existing-content-reflection.md", "faq-reconstruction.md",
 "buyer-trust-and-freshness.md", "entity-alias-and-taxonomy-freshness.md"
]

def test_operational_learning_files_exist():
    for name in REQUIRED:
        assert (ROOT / "knowledge" / name).is_file(), name

def test_version():
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "1.1.2"
