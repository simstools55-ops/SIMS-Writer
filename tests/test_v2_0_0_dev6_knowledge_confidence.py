from datetime import date
from pathlib import Path
from runtime.sims_writer_runtime.knowledge_confidence import knowledge_confidence, publication_ceiling, freshness_status
from runtime.sims_writer_runtime.progressive_editing import progressive_decision
ROOT=Path(__file__).resolve().parents[1]

def test_assets_and_version():
    assert (ROOT/'runtime/knowledge-confidence-freshness-v2.0.md').exists()
    assert (ROOT/'VERSION').read_text().strip()=='3.0.0'

def test_official_current_can_be_public_ok():
    r={'source_level':'OFFICIAL','verified_at':'2026-07-20','max_age_days':90}
    assert knowledge_confidence(r,today=date(2026,7,26))==100
    assert publication_ceiling(r,today=date(2026,7,26))=='PUBLIC_OK'

def test_multiple_third_party_is_user_decision_for_spec_claim():
    r={'source_level':'MULTIPLE_THIRD_PARTY','verified_at':'2026-07-20','max_age_days':90}
    assert publication_ceiling(r,today=date(2026,7,26))=='USER_DECISION'

def test_stale_official_is_not_public_ok():
    r={'source_level':'OFFICIAL','verified_at':'2023-01-01','max_age_days':365}
    assert freshness_status(r,today=date(2026,7,26))=='stale'
    assert publication_ceiling(r,today=date(2026,7,26))=='INTERNAL_REJECT'

def test_progressive_respects_knowledge_ceiling():
    c={'component':'faq','change_basis':'serp_gap','evidence_level':'HIGH','source_level':'MULTIPLE_THIRD_PARTY','verified_at':'2026-07-20','max_age_days':90}
    assert progressive_decision(c,serp_status='verified')=='USER_DECISION'
