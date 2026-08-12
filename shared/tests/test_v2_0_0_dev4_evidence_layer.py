from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_dev4_evidence_assets():
    assert (ROOT/'knowledge/integrated-serp-query-evidence.md').exists()
    assert (ROOT/'validation/evidence-contamination-validation.md').exists()
    assert (ROOT/'quality/EVIDENCE_DECISION_POLICY_V2.md').exists()
    assert (ROOT/'VERSION').read_text(encoding='utf-8').strip()=='3.5.0'
