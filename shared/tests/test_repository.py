from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "VERSION",
    "CHANGELOG.md",
    "knowledge/intent-analysis.md",
    "knowledge/hidden-anxiety.md",
    "knowledge/evidence-transparency.md",
    "knowledge/serp-entity-preservation.md",
    "knowledge/internal-link-semantics.md",
    "knowledge/decision-support.md",
    "knowledge/freshness-safety.md",
    "mappings/writer/application-mapping.md",
    "mappings/article-creator/application-mapping.md",
    "validation/shared-knowledge-validation.md",
    "docs/integration-policy.md",
]


def test_required_files_exist():
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    assert not missing, f"Missing required files: {missing}"


def test_version_is_current():
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "1.1.2"


def test_no_empty_markdown_files():
    empty = [str(p.relative_to(ROOT)) for p in ROOT.rglob("*.md") if not p.read_text(encoding="utf-8").strip()]
    assert not empty, f"Empty markdown files: {empty}"
