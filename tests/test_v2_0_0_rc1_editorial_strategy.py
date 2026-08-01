from pathlib import Path
from runtime.sims_writer_runtime.editorial_strategy import select_editorial_strategy, attach_strategy, STRATEGY_SERP_GAP, STRATEGY_CTR
from runtime.sims_writer_runtime.editorial_decision import build_publication_result
ROOT=Path(__file__).resolve().parents[1]

def test_version_and_contract4():
 assert (ROOT/'VERSION').read_text().strip()=='3.0.2'
 import json
 s=json.loads((ROOT/'schemas/SIMS_FEEDBACK_V2.schema.json').read_text())
 assert s['properties']['contract_version']['const']=='4.2'
 assert 'information' not in s['properties']

def test_strategy_selection_deep_rank_gap():
 s=select_editorial_strategy({'average_position':52.2,'impressions':66,'ctr':0,'intent_match':'match','supported_gap_count':2})
 assert s['strategy']==STRATEGY_SERP_GAP

def test_strategy_selection_top_rank_low_ctr():
 s=select_editorial_strategy({'average_position':2.5,'impressions':5000,'ctr':0.005,'intent_match':'match'})
 assert s['strategy']==STRATEGY_CTR

def test_strategy_scope_rejects_unrelated_change():
 strategy=select_editorial_strategy({'average_position':2.5,'impressions':5000,'ctr':0.005,'intent_match':'match'})
 changes=[{'component':'body','before':'a','after':'b','evidence_level':'HIGH','copy_ready':True}]
 r=build_publication_result(changes,strategy=strategy)
 assert not r['public_ok_changes']
 assert r['_internal_rejected_changes']

def test_strategy_stays_internal():
 strategy=select_editorial_strategy({'average_position':52.2,'supported_gap_count':1})
 r=build_publication_result([{'component':'faq','before':'a','after':'b','evidence_level':'HIGH','copy_ready':True}],strategy=strategy)
 assert '_internal_editorial_strategy' in r
 assert all('editorial_strategy' not in x for x in r['public_ok_changes'])
