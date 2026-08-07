import json
from pathlib import Path

from runtime.sims_writer_runtime.contract_router import (
    expected_output_contract, build_treatment_result_v1, validate_output_contract_for_request
)


def a000043_request():
    return {
        "format":"SIMS_WRITER_TREATMENT_REQUEST_V1",
        "contract_version":"1.0",
        "case_id":"CASE-20260808-A000043-001",
        "article_id":"A000043",
        "site_id":"chiebukuro55",
        "request_mode":"DOCTOR_REFERRAL_TREATMENT",
        "article":{"url":"https://chiebukuro55.com/1545"},
        "doctor_referral":{"allowed_scope":["OS_VERSION_FACT_UPDATE","DATE_REFERENCE_UPDATE"],"blocked_scope":["FULL_REWRITE","TITLE_CHANGE"]},
        "return_contract":{"format":"SIMS_WRITER_TREATMENT_RESULT_V1","contract_version":"1.0","return_to":"SIMS_BLOG_MANAGER"},
    }


def test_a000043_routes_to_treatment_result():
    assert expected_output_contract(a000043_request()) == ("SIMS_WRITER_TREATMENT_RESULT_V1","1.0")


def test_a000043_feedback_v2_is_blocked():
    issues=validate_output_contract_for_request(a000043_request(), {"format":"SIMS_FEEDBACK_V2","contract_version":"4.2"})
    assert issues
    assert "SIMS_WRITER_TREATMENT_RESULT_V1" in issues[0]


def test_a000043_treatment_result_is_accepted():
    publication={"status":"PUBLIC_OK","change_summary":["OS表記を更新"],"public_ok_changes":[{"target":"meta_description","before":"2026年3月","after":"2026年8月","reason":"鮮度更新"}],"user_decision_changes":[]}
    result=build_treatment_result_v1(request=a000043_request(),publication_result=publication,completed_at="2026-08-08T08:10:00+09:00",recommended_review_days=35,next_action="remeasure")
    assert result["format"]=="SIMS_WRITER_TREATMENT_RESULT_V1"
    assert result["case_id"]=="CASE-20260808-A000043-001"
    assert result["publication_result"]==publication
    assert validate_output_contract_for_request(a000043_request(),result)==[]


def test_standard_request_keeps_feedback_v2():
    req={"format":"SIMS_WRITER_IMPROVEMENT_REQUEST_V1","request_mode":"STANDARD"}
    assert expected_output_contract(req)==("SIMS_FEEDBACK_V2","4.2")
