from pathlib import Path
from runtime.sims_writer_runtime.schema_normalizer import normalize_feedback
from runtime.sims_writer_runtime.localization import user_facing_term


def test_legacy_contract_fields_are_canonicalized():
    out=normalize_feedback({
      "diagnosis":{"code":"LOW_SAMPLE","main_query":"sample query"},
      "changes":[{"target":"description","implementation_status":"implemented","before":"old","after":"new","reason":"fix"}],
      "expected_effect":{"ctr":"possible","clicks":""},
      "validation":{"checks":[{"code":"VAL-X","status":"PASS","message":""}]},
      "publication_qa":{"contract":"EDITORIAL_QA_CONTRACT_V1","initial_verdict":"PASS","final_verdict":"PASS","auto_fix_applied":True,"review_trace":"checked","unresolved_findings":["確認待ち"]}
    })
    assert out["main_query"]=="sample query"
    assert out["changes"][0]["component"]=="meta_description"
    assert "clicks" not in out["expected_effect"]
    assert out["publication_qa"]["contract"]=="SIMS_EDITORIAL_QA_V1"
    assert "auto_fix_applied" not in out["publication_qa"]
    assert out["publication_qa"]["auto_fixes"]
    assert isinstance(out["publication_qa"]["review_trace"],list)
    assert out["publication_qa"]["final_verdict"]=="PASS_WITH_WARNING"


def test_internal_link_aliases_are_normalized():
    out=normalize_feedback({"internal_link_evaluation":[{"candidate_url":"https://example.com","status":"held","reason":"check"}]})
    row=out["internal_link_evaluation"][0]
    assert row["url"]=="https://example.com"
    assert row["decision"]=="held"
    assert row["implementation_status"]=="not_implemented"


def test_japanese_terms_cover_remaining_user_terms():
    assert user_facing_term("LOW_COVERAGE",True)=="取得範囲が限定的（LOW_COVERAGE）"
    assert user_facing_term("Change Budget",False)=="変更量の上限"
    assert user_facing_term("graceful_degradation",False)=="情報不足時の保守的処理"


def test_release_cleaner_has_no_cache_patterns_missing():
    root=Path(__file__).resolve().parents[2]
    text=(root/"tools/release_cleaner.py").read_text(encoding="utf-8")
    for token in (".pytest_cache","__pycache__","*.pyc" if False else ".pyc","Thumbs.db"):
        assert token in text
