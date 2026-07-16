from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from runtime.sims_writer_runtime.vertical_slices.ctr_improvement import CTRImprovementSlice
from runtime.sims_writer_runtime.quality.engine import QualityValidationEngine

def test_ctr_vertical_slice():
    raw=json.loads((ROOT/'examples/vertical-slices/ctr-improvement/sbm-request.json').read_text(encoding='utf-8'))
    s=CTRImprovementSlice(); req=s.normalize(raw); dec=s.decide(req); draft=s.build_draft(req,dec)
    assert dec.title_action=='revise'
    assert 'wi-fi' in draft['seo_title'].lower()
    assert draft['introduction']
    assert len(draft['faq'])==2
    report=QualityValidationEngine(ROOT).evaluate(draft,{'main_query':req['main_query'],'model_assisted_checks':draft['model_assisted_checks']})
    assert report['rules_evaluated']==42
    assert len(report['gate_results'])==7
    assert report['publish_recommendation'] in ('publish_ready','publish_ready_with_advisory')
