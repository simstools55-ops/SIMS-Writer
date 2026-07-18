from runtime.sims_writer_runtime.audit import run_audit
def test_title_topic_mismatch_detected():
    s=run_audit({"seo_title":"Windows設定方法","body_topic":"iPhone"})
    assert "CONSISTENCY_TITLE_TOPIC_MISMATCH" in s.warnings
