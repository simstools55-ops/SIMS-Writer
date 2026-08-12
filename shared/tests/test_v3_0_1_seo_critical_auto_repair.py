from pathlib import Path

def test_v301_policy_and_validation_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "quality/SEO_CRITICAL_VALIDATION_AND_AUTO_REPAIR_V3_0_1.md").exists()
    assert (root / "validation/seo-critical-auto-repair-validation.md").exists()
