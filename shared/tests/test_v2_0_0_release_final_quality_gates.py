from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_release_final_safety_assets_exist():
    text = (ROOT / "knowledge/semantic-expectation-ymyl-safety.md").read_text(encoding="utf-8")
    assert "Semantic title rule" in text
    assert "YMYL safety rule" in text
    assert (ROOT / "validation/release-final-quality-gates.md").exists()
