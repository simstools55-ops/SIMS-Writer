from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_version_350():
    assert (ROOT/'VERSION').read_text(encoding='utf-8').strip()=='3.5.0'
    assert json.loads((ROOT/'PRODUCT_IDENTITY.json').read_text(encoding='utf-8'))['current_version']=='3.5.0'
    assert json.loads((ROOT/'PLATFORM_MANIFEST.json').read_text(encoding='utf-8'))['shared_version']=='3.5.0'

def test_presentation_framework_files_exist():
    for name in ['HUMAN_EXPERIENCE_ARCHITECTURE_V1.md','PRESENTATION_STANDARD_V1.md','HUMAN_OUTPUT_POLICY_V1.md','MACHINE_OUTPUT_POLICY_V1.md','HUMAN_USABILITY_GATE_V1.md']:
        assert (ROOT/'presentation'/name).exists()

def test_all_products_in_scope_and_staged_rollout():
    t=(ROOT/'presentation'/'HUMAN_EXPERIENCE_ARCHITECTURE_V1.md').read_text(encoding='utf-8')
    for token in ['SBM','Doctor','Writer','Creator','Merge']:
        assert token in t
    assert 'RC3先行適用: Doctor / SBM / Writer' in t
    assert 'Specification-only adoption: Creator / Merge' in t

def test_writer_before_after_not_optional_for_doctor_referral():
    t=(ROOT/'presentation'/'PRESENTATION_STANDARD_V1.md').read_text(encoding='utf-8')
    for token in ['Before','After','reason','expected_effect','DOCTOR_REFERRAL_TREATMENT']:
        assert token in t

def test_internal_fields_hidden_from_human_output():
    t=(ROOT/'presentation'/'HUMAN_OUTPUT_POLICY_V1.md').read_text(encoding='utf-8')
    for token in ['allowed_scope','blocked_scope','Routing','Contract']:
        assert token in t
    assert '通常説明には出さない' in t

def test_machine_fields_preserved():
    t=(ROOT/'presentation'/'MACHINE_OUTPUT_POLICY_V1.md').read_text(encoding='utf-8')
    for token in ['Evidence','allowed_scope','blocked_scope','actions_permitted','actions_prohibited','Routing']:
        assert token in t

def test_registry_has_presentation():
    d=json.loads((ROOT/'registries/platform-registry.json').read_text(encoding='utf-8'))
    assert any(x['id']=='REG-PRESENTATION' and x['path']=='presentation/' for x in d['registries'])
