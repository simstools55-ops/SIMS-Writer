from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
def test_schema_and_presentation():
    s=json.loads((ROOT/'contracts/json/SIMS_FEEDBACK_V2.schema.json').read_text(encoding='utf-8'))
    assert s['properties']['format']['const']=='SIMS_FEEDBACK_V2'
    assert s['properties']['diagnosis']['type']=='array'
    assert 'INTENT_MISMATCH' in s['properties']['diagnosis']['items']['enum']
    p=(ROOT/'presentation/PRESENTATION_TEMPLATE.md').read_text(encoding='utf-8')
    assert 'overflow-y:auto' in p and 'max-height:24rem' in p
def test_runtime_rules():
    d=(ROOT/'runtime/search-diagnosis.md').read_text(encoding='utf-8')
    assert 'INTENT_MISMATCH' in d and 'POSITION_OPPORTUNITY' in d
