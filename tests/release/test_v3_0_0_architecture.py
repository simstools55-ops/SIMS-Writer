from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]

def test_version_and_assets():
    assert (ROOT/'VERSION').read_text().strip()=='3.0.2'
    for p in ['runtime/pipeline/05a-temporal_lifecycle_analysis.md','knowledge/sets/KS-TMP-001-temporal-lifecycle.yaml','patterns/definitions/planning/PT-PLN-008-temporal-lifecycle-recovery.yaml','shared/knowledge/content-lifecycle.md']:
        assert (ROOT/p).exists(), p

def test_feedback_extension_is_optional():
    s=json.loads((ROOT/'contracts/json/SIMS_FEEDBACK_V2.schema.json').read_text(encoding='utf-8'))
    assert 'analysis_extensions' in s['properties']
    assert 'analysis_extensions' not in s.get('required',[])
