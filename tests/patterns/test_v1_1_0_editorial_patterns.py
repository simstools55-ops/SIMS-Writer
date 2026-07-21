import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
IDS={"PT-PLN-008","PT-PLN-009","PT-SEO-008","PT-SEO-009","PT-EVD-007","PT-SEC-009"}

def test_editorial_patterns_registered_and_present():
    reg=json.loads((ROOT/"patterns/registry/pattern-registry.json").read_text(encoding="utf-8"))
    by_id={x["id"]:x for x in reg["patterns"]}
    assert IDS <= set(by_id)
    for pid in IDS:
        assert (ROOT/by_id[pid]["path"]).is_file()

def test_editorial_patterns_preserve_writer_constraints():
    reg=json.loads((ROOT/"patterns/registry/pattern-registry.json").read_text(encoding="utf-8"))
    by_id={x["id"]:x for x in reg["patterns"]}
    for pid in IDS:
        data=json.loads((ROOT/by_id[pid]["path"]).read_text(encoding="utf-8"))
        assert "preservation_guard_passed" in data["applicability"]["conditions"]
        assert "change_budget_exceeded" in data["non_applicability"]
