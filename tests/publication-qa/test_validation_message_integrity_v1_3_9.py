import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from runtime.sims_writer_runtime.schema_normalizer import normalize_feedback
from runtime.sims_writer_runtime.validation_message_gate import enforce_validation_messages, blank_validation_messages

def blank():
    return "".join([])

def test_blank_pass_message_is_replaced_with_rule_specific_text():
    out=normalize_feedback({"validation":{"checks":[{"code":"VAL-FACT-001","status":"PASS","message":blank()}]}})
    msg=out["validation"]["checks"][0]["message"]
    assert msg
    assert "数値" in msg and "確認" in msg
    assert "具体的な確認内容" not in msg

def test_whitespace_message_is_replaced():
    out=normalize_feedback({"validation":{"checks":[{"code":"VAL-INTENT-001","status":"PASS","message":"   "}]}})
    assert "主要検索意図" in out["validation"]["checks"][0]["message"]

def test_generic_placeholder_is_replaced():
    out=normalize_feedback({"validation":{"checks":[dict(code="VAL-LINK-001", status="PASS", message="問題なし")]}})
    assert "URL" in out["validation"]["checks"][0]["message"]

def test_unknown_code_gets_nonblank_auditable_fallback():
    out=normalize_feedback({"validation":{"checks":[{"code":"VAL-CUSTOM-999","status":"WARNING"}]}})
    msg=out["validation"]["checks"][0]["message"]
    assert "VAL-CUSTOM-999" in msg and "WARNING" in msg

def test_final_gate_has_zero_blanks():
    payload={"validation":{"checks":[{"code":"VAL-FACT-001","status":"PASS","message":blank()},{"code":"VAL-LINK-001","status":"PASS"}]}}
    enforce_validation_messages(payload)
    assert blank_validation_messages(payload)==[]

def test_schema_rejects_blank_validation_message():
    root=Path(__file__).resolve().parents[2]
    schema=json.loads((root/"schemas/SIMS_FEEDBACK_V2.schema.json").read_text(encoding="utf-8"))
    assert "validation" not in schema["properties"]
    assert (root/"schemas/SIMS_WRITER_INTERNAL_AUDIT_V1.schema.json").exists()

def test_repository_contains_no_literal_blank_validation_message_examples():
    root=Path(__file__).resolve().parents[2]
    forbidden='"message"' + ': ' + '""'
    hits=[]
    for path in root.rglob("*"):
        if not path.is_file() or any(x in path.parts for x in (".git",".pytest_cache","__pycache__")):
            continue
        if path.suffix.lower() not in {".md",".json",".py",".txt",".yaml",".yml"}:
            continue
        text=path.read_text(encoding="utf-8",errors="ignore")
        if forbidden in text:
            hits.append(str(path.relative_to(root)))
    assert hits==[]
