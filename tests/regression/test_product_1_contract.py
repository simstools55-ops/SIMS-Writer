from jsonschema import Draft202012Validator
import json
from pathlib import Path
from runtime.sims_writer_runtime.audit import run_audit
ROOT=Path(__file__).resolve().parents[2]
def test_feedback_v21_schema():
    base=ROOT/'contracts/sims-feedback/v2.1'
    schema=json.loads((base/'sims-feedback-v2.1.schema.json').read_text())
    store={
      'https://sims-writer.local/contracts/sims-feedback/v2.1/reason-codes.schema.json':json.loads((base/'reason-codes.schema.json').read_text()),
      'https://sims-writer.local/contracts/sims-feedback/v2.1/warning-codes.schema.json':json.loads((base/'warning-codes.schema.json').read_text())}
    from jsonschema import RefResolver
    v=Draft202012Validator(schema,resolver=RefResolver.from_schema(schema,store=store))
    data=run_audit({"runtime_state_id":"r1"}).feedback_json
    assert list(v.iter_errors(data))==[]
