from pathlib import Path

from runtime.sims_writer_runtime.evidence_layer import classify_gap, enforce_evidence_boundaries
from runtime.sims_writer_runtime.editorial_decision import build_publication_result

ROOT=Path(__file__).resolve().parents[1]

def test_evidence_assets_exist():
    for name in ["evidence-layer-v2.0.md","evidence-contamination-qa-v2.0.md","integrated-gap-analysis-v2.0.md"]:
        assert (ROOT/"runtime"/name).exists()

def test_query_serp_without_evidence_is_not_supported_gap():
    gap={"query_signal":True,"serp_signal":True,"serp_status":"verified","evidence_level":"LOW"}
    assert classify_gap(gap)=="DECISION_GAP"

def test_low_evidence_claim_cannot_leak_into_public_ok():
    changes=[
      {"component":"faq","before":"","after":"候補","claims":[{"claim_id":"monthly_limit","evidence_level":"LOW"}],"claim_ids":["monthly_limit"],"editorial_decision":"USER_DECISION"},
      {"component":"introduction","before":"旧","after":"月間上限があります","claim_ids":["monthly_limit"],"editorial_decision":"PUBLIC_OK"},
    ]
    checked,findings=enforce_evidence_boundaries(changes)
    intro=next(x for x in checked if x["component"]=="introduction")
    assert intro["editorial_decision"]=="USER_DECISION"
    assert findings[0]["code"]=="EVIDENCE-CONTAMINATION-001"

def test_publication_result_keeps_evidence_findings_internal():
    changes=[
      {"component":"faq","before":"","after":"候補","claims":[{"claim_id":"x","evidence_level":"LOW"}],"claim_ids":["x"],"editorial_decision":"USER_DECISION"},
      {"component":"meta_description","before":"旧","after":"未確認事項","claim_ids":["x"],"editorial_decision":"PUBLIC_OK"},
    ]
    result=build_publication_result(changes)
    assert result["user_decision_changes"]
    assert result["_internal_evidence_findings"]
    assert not result["public_ok_changes"]
