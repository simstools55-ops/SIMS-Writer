from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def test_sbm_is_case_owner_and_orchestrator():
    contract = read("doctor/INTERFACE_CONTRACTS_V2.md")
    assert "`case_id` is issued and owned by SBM" in contract
    assert "Doctor never directly invokes Writer" in contract
    assert "Writer returns the treatment result to SBM" in contract


def test_legacy_direct_routing_is_deprecated():
    legacy = read("doctor/INTERFACE_CONTRACTS_V1.md")
    assert "Deprecated compatibility document" in legacy
    assert "New implementations must not prefer" in legacy


def test_case_lifecycle_contains_minimum_loop():
    lifecycle = read("doctor/CASE_LIFECYCLE_V1.md")
    for state in [
        "DOCTOR_DIAGNOSIS_PENDING",
        "DOCTOR_DIAGNOSED",
        "WRITER_REQUEST_READY",
        "TREATMENT_RESULT_RECEIVED",
        "MONITORING",
        "REEXAMINATION_PENDING",
        "COMPLETED",
    ]:
        assert state in lifecycle


def test_platform_registry_includes_doctor_contracts():
    registry = json.loads(read("registries/platform-registry.json"))
    assert registry["version"] == "3.5.0"
    assert any(item["id"] == "REG-DOCTOR-PLATFORM" for item in registry["registries"])


def test_safety_boundary_prohibits_direct_specialist_routing():
    boundary = read("doctor/SBM_DOCTOR_SAFETY_BOUNDARY.md")
    assert "Doctor does not invoke Writer, Creator, or Merge directly" in boundary
    assert "Specialist treatment results return to SBM" in boundary
