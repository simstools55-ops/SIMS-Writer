from runtime.sims_writer_runtime.audit import run_audit
def test_critical_assumption_stops_and_rewrites():
    s=run_audit({"critical_assumption_error":True})
    assert s.quality_decision=="stop_and_rewrite"
    assert s.change_scope=="full_rewrite"
