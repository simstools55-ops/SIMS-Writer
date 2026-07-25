import json
from pathlib import Path

from runtime.sims_writer_runtime.editorial_decision import (
    INTERNAL_REJECT, PUBLIC_OK, USER_DECISION, build_publication_result,
    classify_change, user_visible_publication_result,
)
from runtime.sims_writer_runtime.qa.presentation import apply_qa_to_feedback, build_publication_view


def test_change_level_decisions():
    assert classify_change({"before":"旧","after":"新"}) == PUBLIC_OK
    assert classify_change({"before":"旧","after":"新","requires_user_confirmation":True}) == USER_DECISION
    assert classify_change({"before":"旧","after":"","qa_status":"FAIL"}) == INTERNAL_REJECT


def test_internal_reject_is_silent():
    result=build_publication_result([
        {"component":"seo_title","component_label":"SEOタイトル","before":"旧","after":"新"},
        {"component":"body","component_label":"本文","before":"旧","after":"危険","internal_reject":True},
    ])
    public=user_visible_publication_result(result)
    assert len(public["public_ok_changes"]) == 1
    assert "_internal_rejected_changes" not in public


def test_contract_3_excludes_internal_qa():
    qa={"qa_contract":"SIMS_EDITORIAL_QA_V1","qa_engine_version":"1.1.0","initial_verdict":"PASS","final_verdict":"PASS","publishable":True,"release_action":"publish","auto_fix_applied":False,"auto_fixes":[],"review_cycles_used":0,"review_trace":[],"final_draft":{"seo_title":"新"},"refinement_result":{"revision_records":[]},"final_quality_report":{"issues":[]},"final_foundation_report":{"warnings":[]}}
    view=build_publication_view({"seo_title":"旧"},qa)
    feedback=apply_qa_to_feedback({"article_id":"A1","article_url":"https://example.com","information":[]},view)
    assert feedback["contract_version"] == "3.0"
    assert "publication_result" in feedback
    assert "publication_qa" not in feedback
    assert "diagnosis" not in feedback
    assert view["internal_audit_record"]["record_type"] == "SIMS_WRITER_INTERNAL_AUDIT_V1"


def test_contract_schema_is_v3():
    schema=json.loads((Path(__file__).parents[2]/"schemas/SIMS_FEEDBACK_V2.schema.json").read_text(encoding="utf-8"))
    assert schema["properties"]["contract_version"]["const"] == "3.0"
    assert "diagnosis" not in schema["properties"]
