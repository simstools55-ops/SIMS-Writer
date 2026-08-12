import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_shared_version_340():
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() in {"3.5.0", "3.5.0"}
    identity = json.loads((ROOT / "PRODUCT_IDENTITY.json").read_text(encoding="utf-8"))
    assert identity["current_version"] in {"3.5.0", "3.5.0"}
    platform = json.loads((ROOT / "PLATFORM_MANIFEST.json").read_text(encoding="utf-8"))
    assert platform["shared_version"] in {"3.5.0", "3.5.0"}

def test_algorithm_evidence_is_not_diagnosis():
    text = (ROOT / "doctor/ALGORITHM_EVIDENCE_V1.md").read_text(encoding="utf-8")
    assert "Algorithm information is Evidence, not Diagnosis" in text
    assert "アップデート期間との時間的一致だけ" in text
    assert "WAIT" in text

def test_integrated_evidence_reuses_existing_confidence_canon():
    text = (ROOT / "knowledge/integrated-evidence-policy.md").read_text(encoding="utf-8")
    assert "source-confidence-freshness.md" in text
    assert "evidence-confidence-and-contradiction.md" in text
    assert "重複スコア体系を定義しない" in text

def test_treatment_strategy_preserves_sbm_routing():
    text = (ROOT / "doctor/TREATMENT_ROUTING_V1.md").read_text(encoding="utf-8")
    for value in ["WAIT", "LIGHT_FIX", "NORMAL_REWRITE", "FULL_REWRITE"]:
        assert value in text
    assert "Doctor returns it to SBM" in text

def test_interface_contract_keeps_doctor_sbm_specialist_path():
    text = (ROOT / "doctor/INTERFACE_CONTRACTS_V2.md").read_text(encoding="utf-8")
    assert "Doctor -> SBM -> specialist" in text
    assert "Algorithm information is Evidence" in text
