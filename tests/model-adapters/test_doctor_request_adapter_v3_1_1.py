import importlib.util
from pathlib import Path

p=Path(__file__).parents[2]/"runtime"/"adapters"/"doctor_request_adapter.py"
spec=importlib.util.spec_from_file_location("doctor_adapter",p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def test_adapter_preserves_case_and_prohibitions():
    payload={"format":"SIMS_DOCTOR_WRITER_REQUEST_V1","contract_version":"1.0","site":{"site_id":"s"},"case":{"case_id":"C1"},"treatment":{"treatment_id":"T1","executor":"SIMS_WRITER","treatment_type":"REWRITE"},"article":{"article_id":"A1","url":"https://example.com/a"},"editing_scope":{"prohibited_actions":["MERGE_WITH_OTHER_ARTICLE"]}}
    out=m.adapt_doctor_request(payload)
    assert out["case_id"]=="C1" and out["treatment_id"]=="T1"
    assert "CHANGE_URL" in out["hard_prohibitions"]
