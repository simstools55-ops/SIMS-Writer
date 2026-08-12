from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_dev6_assets():
    assert (ROOT/'quality/KNOWLEDGE_CONFIDENCE_FRESHNESS_V2.md').exists()
    assert (ROOT/'validation/knowledge-confidence-validation.md').exists()
    assert (ROOT/'VERSION').read_text().strip()=='3.5.0'
