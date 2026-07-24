import json
from pathlib import Path

def root(): return Path(__file__).resolve().parents[2]

def test_official_suite_profiles_are_complete():
    suite=root()/"tests/regression/official-v1"
    manifest=json.loads((suite/"manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["cases"])==5
    for item in manifest["cases"]:
        spec=json.loads((suite/item["case_spec"]).read_text(encoding="utf-8"))
        assert spec["fixture_status"]=="awaiting_source_artifacts"
        assert spec["required_findings"]
        assert spec["permitted_auto_fixes"]
        assert spec["expected_initial_verdict"] in {"PASS","PASS_WITH_WARNING","PASS_WITH_MINOR_FIX","PASS_WITH_REQUIRED_FIX","FAIL"}

def test_evaluation_standard_exists():
    text=(root()/"product/quality/QA_EVALUATION_STANDARD.md").read_text(encoding="utf-8")
    for term in ["Winner Query","Numeric","Contract","Validation","Auto-fix"]:
        assert term.lower() in text.lower()
