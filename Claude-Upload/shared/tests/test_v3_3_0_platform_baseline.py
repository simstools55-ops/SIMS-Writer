from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_version_and_identity():
    assert (ROOT/'VERSION').read_text().strip()=='3.5.0'
    identity=json.loads((ROOT/'PRODUCT_IDENTITY.json').read_text())
    assert identity['product_code']=='SHARED'
    assert identity['current_version']=='3.5.0'

def test_platform_contracts_exist_and_parse():
    required=[
      'contracts/common/common-envelope-v1.schema.json',
      'contracts/doctor/doctor-diagnosis-request-v1.schema.json',
      'contracts/doctor/doctor-diagnosis-result-v1.schema.json',
      'contracts/writer/writer-treatment-request-v1.schema.json',
      'contracts/writer/writer-treatment-result-v1.schema.json',
      'contracts/creator/creator-treatment-request-v1.schema.json',
      'contracts/creator/creator-treatment-result-v1.schema.json',
      'contracts/merge/merge-treatment-request-v1.schema.json',
      'contracts/merge/merge-treatment-result-v1.schema.json',
      'contracts/platform/publication-result-v1.schema.json',
      'contracts/platform/monitoring-result-v1.schema.json',
      'contracts/platform/platform-case-event-v1.schema.json',
      'contracts/platform/platform-error-v1.schema.json']
    for rel in required:
      p=ROOT/rel; assert p.exists(), rel; json.loads(p.read_text())

def test_enums_and_snapshot_scopes():
    for name in ['product-code','case-status','treatment-type','result-status','diagnosis-code']:
      data=json.loads((ROOT/'enums'/f'{name}.json').read_text()); assert data['values']
    for target in ['sbm','doctor','writer','creator','merge']:
      data=json.loads((ROOT/'snapshots'/target/'SNAPSHOT_SCOPE.json').read_text()); assert data['source_version']=='3.5.0'

def test_merge_safety_baseline():
    text=(ROOT/'knowledge/merge/MERGE_VALIDATION.md').read_text()
    assert 'rollback' in text.lower()
    assert 'user approval' in text.lower()
