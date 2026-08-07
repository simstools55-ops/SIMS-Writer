import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_writer_identity_and_versions():
    identity = json.loads((ROOT / "PRODUCT_IDENTITY.json").read_text(encoding="utf-8"))
    assert identity["product_code"] == "WRITER"
    assert identity["repository_name"] == "SIMS-Writer"
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "3.3.1-RC3"
    assert (ROOT / "SHARED_VERSION").read_text(encoding="utf-8").strip() == "3.5.0"


def test_platform_contracts_parse():
    paths = [
        ROOT / "shared/contracts/common/common-envelope-v1.schema.json",
        ROOT / "shared/contracts/writer/writer-treatment-request-v1.schema.json",
        ROOT / "shared/contracts/writer/writer-treatment-result-v1.schema.json",
        ROOT / "shared/contracts/platform/publication-result-v1.schema.json",
    ]
    for path in paths:
        assert path.exists(), path
        json.loads(path.read_text(encoding="utf-8"))


def test_doctor_implementation_not_embedded():
    assert not (ROOT / "src/doctor").exists()
    assert not (ROOT / "claude").exists()
    assert not list((ROOT / "contracts").glob("SIMS_DOCTOR_*.schema.json"))
