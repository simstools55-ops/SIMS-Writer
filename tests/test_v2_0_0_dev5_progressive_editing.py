from pathlib import Path

from runtime.sims_writer_runtime.progressive_editing import progressive_decision, apply_progressive_editing
from runtime.sims_writer_runtime.editorial_decision import build_publication_result

ROOT=Path(__file__).resolve().parents[1]

def test_assets_and_version():
    assert (ROOT/'runtime/progressive-editing-engine-v2.0.md').exists()
    assert (ROOT/'VERSION').read_text().strip()=='2.0.0-release-candidate.2'

def test_partial_allows_supported_meta():
    c={'component':'meta_description','change_basis':'usability','evidence_level':'HIGH','after':'完成メタ','before':'途中...'}
    assert progressive_decision(c,serp_status='partial')=='PUBLIC_OK'

def test_partial_allows_supported_title_without_new_promise():
    c={'component':'seo_title','change_basis':'search_intent','evidence_level':'MEDIUM','after':'新','before':'旧','serp_gap_required':False,'introduces_new_claim':False}
    assert progressive_decision(c,serp_status='partial')=='PUBLIC_OK'

def test_partial_sends_supported_faq_to_user_decision():
    c={'component':'faq','change_basis':'serp_gap','evidence_level':'MEDIUM','after':'候補','before':''}
    assert progressive_decision(c,serp_status='partial')=='USER_DECISION'

def test_partial_rejects_new_claim_in_intro_when_none():
    c={'component':'introduction','change_basis':'serp_gap','evidence_level':'NONE','after':'未確認事項','before':'旧','introduces_new_claim':True}
    assert progressive_decision(c,serp_status='partial')=='INTERNAL_REJECT'

def test_component_scoping_keeps_safe_change():
    changes=[
      {'component':'meta_description','change_basis':'usability','evidence_level':'HIGH','before':'途中...','after':'完成'},
      {'component':'body','change_basis':'serp_gap','evidence_level':'NONE','before':'旧','after':'未確認追加'},
    ]
    result=build_publication_result(changes,serp_status='partial')
    assert [x['component'] for x in result['public_ok_changes']]==['meta_description']
    assert not result['user_decision_changes']
    assert len(result['_internal_rejected_changes'])==1
    assert result['_internal_progressive_trace']
