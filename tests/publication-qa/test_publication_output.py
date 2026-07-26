from runtime.sims_writer_runtime.qa.presentation import apply_qa_to_feedback, build_publication_view


def qa_result(verdict="PASS_WITH_MINOR_FIX", publishable=True):
    return {
        "qa_contract": "SIMS_EDITORIAL_QA_V1",
        "qa_engine_version": "1.1.0",
        "final_verdict": verdict,
        "publishable": publishable,
        "release_action": "publish_corrected_version" if publishable else "hold_and_revise",
        "auto_fix_applied": True,
        "review_cycles_used": 1,
        "final_draft": {"seo_title": "修正版", "article_content": "修正後本文"},
        "refinement_result": {"revision_records": [{"routes": [{"recovery_type": "placeholder_elimination"}]}]},
        "final_quality_report": {"issues": []},
        "final_foundation_report": {"warnings": []},
    }


def test_publication_view_exposes_only_final_publishable_content():
    view = build_publication_view({"seo_title": "元", "article_content": "TODO"}, qa_result())
    assert view["publication_content"]["seo_title"] == "修正版"
    assert view["held_draft"] is None
    assert [x["component"] for x in view["qa_changes"]] == ["seo_title", "article_content"]
    assert view["public_message"].startswith("軽微な修正")


def test_required_fix_holds_content_from_publication():
    result = qa_result("PASS_WITH_REQUIRED_FIX", False)
    view = build_publication_view({"seo_title": "元"}, result)
    assert view["publication_content"] is None
    assert view["held_draft"]["seo_title"] == "修正版"
    assert "公開しない" in view["public_message"]


def test_feedback_extension_is_backward_compatible():
    original = {"format": "SIMS_FEEDBACK_V2", "contract_version": "2.1"}
    view = build_publication_view({"seo_title": "元"}, qa_result())
    merged = apply_qa_to_feedback(original, view)
    assert merged["format"] == "SIMS_FEEDBACK_V2"
    assert merged["contract_version"] == "4.0"
    assert merged["publication_result"]["public_ok_changes"]
