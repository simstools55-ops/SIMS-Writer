from runtime.sims_writer_runtime.qa.severity import revenue_tier, split_issues
from runtime.sims_writer_runtime.editorial_decision import classify_change, INTERNAL_REJECT, USER_DECISION

def test_minor_style_is_non_blocking():
    assert revenue_tier({"severity":"minor","rule_id":"STYLE-001"}) == "non_blocking_quality"

def test_winner_query_risk_is_critical():
    assert revenue_tier({"severity":"minor","rule_id":"QF-WQP-001"}) == "revenue_or_safety_critical"

def test_auto_repairable_issue_is_auto_repair():
    assert revenue_tier({"severity":"warning","auto_repairable":True}) == "auto_repair"

def test_low_evidence_is_internal_not_user_decision():
    change={"before":"a","after":"b","evidence_level":"LOW","copy_ready":True}
    assert classify_change(change) == INTERNAL_REJECT

def test_genuine_owner_choice_is_user_decision():
    change={"before":"a","after":"b","evidence_level":"HIGH","copy_ready":True,"decision_signals":["strategic_tradeoff"]}
    assert classify_change(change) == USER_DECISION

def test_split_includes_revenue_tiers():
    result=split_issues([{"rule_id":"QF-DRIFT-001","severity":"minor"},{"rule_id":"STYLE-001","severity":"minor"}])
    assert len(result["revenue_or_safety_critical"]) == 1
    assert len(result["non_blocking_quality"]) == 1
