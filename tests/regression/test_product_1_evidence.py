from runtime.sims_writer_runtime.audit import run_audit
def test_missing_source_is_warning():
    s=run_audit({"claims":[{"text":"価格は100円"}]})
    assert "EVIDENCE_SOURCE_MISSING" in s.warnings
