from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from runtime.sims_writer_runtime.output_contract import OutputContractValidator, build_feedback, package_output
from runtime.sims_writer_runtime.vertical_slices.ctr_improvement import CTRImprovementSlice


def test_partial_mode_excludes_article_content_and_keeps_feedback_last_layer():
    changes=[{"component":"seo_title","before":"旧","after":"新","reason":"改善"}]
    feedback=build_feedback(article_id="A1",article_url="https://example.com",main_query="test query",before_after=changes,summary="title changed",warnings=[])
    package=package_output(output_mode="partial",before_after=changes,feedback=feedback,article_content="full article")
    assert "article_content" not in package
    assert package["feedback"]["changes"]["seo_title"] is True
    assert OutputContractValidator().validate(package)==[]


def test_body_addition_forces_body_true():
    additions=[{"heading":"new section","content":"new body"}]
    feedback=build_feedback(article_id="A1",article_url="",main_query="query",before_after=[],summary="body added",warnings=[],body_additions=additions)
    package=package_output(output_mode="partial",before_after=[],feedback=feedback,body_additions=additions)
    assert package["feedback"]["changes"]["body"] is True


def test_missing_main_query_is_inferred_without_annotation_in_field():
    raw={"ArticleID":"A000008","URL":"https://example.com","ArticleTitle":"Product AとProduct Bを5つの項目で比較！","SEOTitle":"Product AとProduct Bを5つの項目で比較！ | Site","ExistingContent":"比較本文です。"*30}
    s=CTRImprovementSlice(); req=s.normalize(raw); dec=s.decide(req); draft=s.build_draft(req,dec); package=s.build_output(req,dec,draft)
    assert req["main_query"]=="Product AとProduct B 比較"
    assert "推定" not in package["feedback"]["new_values"]["main_query"]
    assert any("推定" in x for x in package["feedback"]["warnings"])


def test_unverified_adopted_internal_link_is_rejected():
    feedback=build_feedback(article_id="A1",article_url="",main_query="query",before_after=[],summary="",warnings=[])
    feedback["changes"]["internal_links"]=True
    bad={"output_mode":"partial","user_output":[],"internal_link_report":[{"classification":"adopted","verified":False,"applied":True}],"unresolved_items":[],"body_additions":[],"feedback":feedback,"effect_evidence":{}}
    assert any(i.code=="OUT-007" for i in OutputContractValidator().validate(bad))


def _base_feedback(title="短いSEOタイトル", description="短い説明文"):
    fb=build_feedback(article_id="A1",article_url="",main_query="query",before_after=[],summary="",warnings=[])
    fb["new_values"]["seo_title"]=title
    fb["new_values"]["description"]=description
    return fb

def test_forbidden_greeting_or_honorific_is_rejected():
    package={"output_mode":"partial","user_output":[],"rendered_user_output":"マスター、改善結果です。","internal_link_report":[],"unresolved_items":[],"body_additions":[],"feedback":_base_feedback(),"effect_evidence":{}}
    assert any(i.code=="OUT-011" for i in OutputContractValidator().validate(package))

def test_seo_title_and_description_hard_limits_are_enforced():
    package={"output_mode":"partial","user_output":[],"internal_link_report":[],"unresolved_items":[],"body_additions":[],"feedback":_base_feedback("あ"*46,"い"*141),"effect_evidence":{}}
    codes={i.code for i in OutputContractValidator().validate(package)}
    assert {"OUT-012","OUT-014"} <= codes

def test_recommended_length_generates_warning_not_error():
    package={"output_mode":"partial","user_output":[],"internal_link_report":[],"unresolved_items":[],"body_additions":[],"feedback":_base_feedback("あ"*41,"い"*121),"effect_evidence":{}}
    issues=OutputContractValidator().validate(package)
    assert {"OUT-013","OUT-015"} <= {i.code for i in issues}
    OutputContractValidator().assert_valid(package)

def test_response_must_end_with_single_json_code_block():
    valid='改善結果\n\n```json\n{"schema":"SIMS_FEEDBACK_V1"}\n```'
    package={"output_mode":"partial","user_output":[],"rendered_response":valid,"internal_link_report":[],"unresolved_items":[],"body_additions":[],"feedback":_base_feedback(),"effect_evidence":{}}
    assert not any(i.code in {"OUT-016","OUT-017"} for i in OutputContractValidator().validate(package))
    package["rendered_response"] = valid + "\n追記"
    assert any(i.code=="OUT-016" for i in OutputContractValidator().validate(package))
