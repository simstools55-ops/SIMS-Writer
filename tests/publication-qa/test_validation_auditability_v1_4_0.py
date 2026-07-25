from runtime.sims_writer_runtime.schema_normalizer import normalize_feedback


def test_validation_defaults_are_concise_and_specific():
    out=normalize_feedback({"validation":{"checks":[{"code":"VAL-PRESERVE-001","status":"PASS","message":" "}]}})
    msg=out["validation"]["checks"][0]["message"]
    assert 20 <= len(msg) <= 80
    assert "保護対象" in msg


def test_review_trace_is_compact_and_cycles_sync():
    out=normalize_feedback({"publication_qa":{
      "contract":"SIMS_EDITORIAL_QA_V1","initial_verdict":"PASS_WITH_WARNING","final_verdict":"PASS_WITH_WARNING",
      "publishable":True,"release_action":"publish_with_advisory","review_cycles_used":1,"auto_fixes":[],
      "review_trace":[{"cycle":1,"focus":"winner_query・numeric","result":"warning"},{"cycle":2,"finding":"fixed","action":"rewrite","result":"pass"}],
      "unresolved_findings":[]}})
    qa=out["publication_qa"]
    assert qa["review_cycles_used"] == 2
    assert qa["review_trace"][0]["checked"] == ["winner_query","numeric"]
    assert qa["review_trace"][1]["findings"] == ["fixed"]


def test_auto_fix_target_normalizes_to_component():
    out=normalize_feedback({"publication_qa":{
      "contract":"SIMS_EDITORIAL_QA_V1","initial_verdict":"PASS","final_verdict":"PASS",
      "publishable":True,"release_action":"publish","review_cycles_used":1,
      "auto_fixes":[{"target":"meta_description","action":"shorten"}],
      "review_trace":[{"cycle":1,"checked":["meta"],"result":"pass"}],"unresolved_findings":[]}})
    assert out["publication_qa"]["auto_fixes"][0]["component"] == "meta_description"
    assert "target" not in out["publication_qa"]["auto_fixes"][0]
