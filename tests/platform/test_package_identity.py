import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_package_identity():
    identity = json.loads((ROOT / "PRODUCT_IDENTITY.json").read_text(encoding="utf-8"))
    assert identity["product_code"] == "WRITER"
    assert identity["repository_type"] == "CLAUDE_PACKAGE"
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "3.3.2-RC2"
    assert (ROOT / "SHARED_VERSION").read_text(encoding="utf-8").strip() == "3.5.0"


def test_manifest_and_contracts_parse():
    json.loads((ROOT / "CLAUDE_PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    for path in (ROOT / "shared/contracts").rglob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
