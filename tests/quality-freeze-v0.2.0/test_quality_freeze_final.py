from pathlib import Path
import json
import hashlib
import jsonschema

ROOT = Path(__file__).resolve().parents[2]
CLAUDE = ROOT.parent / "SIMS-Writer-Claude-v0.2.0-Quality-Freeze-Final"


def test_required_modules_exist():
    required = [
        ROOT / "validation/VALIDATION_LAYER.md",
        ROOT / "presentation/PRESENTATION_TEMPLATE.md",
        ROOT / "contracts/json/JSON_CONTRACT_v2.md",
        ROOT / "contracts/json/SIMS_FEEDBACK_V2.schema.json",
        CLAUDE / "validation/VALIDATION_LAYER.md",
        CLAUDE / "presentation/PRESENTATION_TEMPLATE.md",
        CLAUDE / "contracts/json/JSON_CONTRACT_v2.md",
        CLAUDE / "contracts/json/SIMS_FEEDBACK_V2.schema.json",
    ]
    assert all(p.exists() for p in required)


def test_schema_is_valid():
    schema = json.loads((ROOT / "contracts/json/SIMS_FEEDBACK_V2.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)


def test_examples_validate():
    schema = json.loads((ROOT / "contracts/json/SIMS_FEEDBACK_V2.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    for path in sorted((ROOT / "examples/feedback-v2").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        errors = list(validator.iter_errors(payload))
        assert not errors, f"{path.name}: {errors}"


def test_core_and_claude_schema_identical():
    a = (ROOT / "contracts/json/SIMS_FEEDBACK_V2.schema.json").read_bytes()
    b = (CLAUDE / "contracts/json/SIMS_FEEDBACK_V2.schema.json").read_bytes()
    assert hashlib.sha256(a).digest() == hashlib.sha256(b).digest()


def test_v2_is_mandatory_in_claude_instructions():
    text = (CLAUDE / "CLAUDE_PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")
    assert "SIMS_FEEDBACK_V2" in text
    assert "validation/VALIDATION_LAYER.md" in text
    assert "presentation/PRESENTATION_TEMPLATE.md" in text
