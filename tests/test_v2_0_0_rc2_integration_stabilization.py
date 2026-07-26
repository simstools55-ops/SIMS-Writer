from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = [
    ROOT/'claude/CLAUDE_PROJECT_INSTRUCTIONS.md',
    ROOT/'claude/PROJECT_INSTRUCTIONS_TO_PASTE.md',
    ROOT/'claude/PUBLICATION_PIPELINE_LOCK.md',
    ROOT/'claude/FINAL_OUTPUT_INTEGRATION_INSTRUCTIONS.md',
    ROOT/'claude/contracts/output-contract.md',
    ROOT/'claude/runtime/output-pipeline.md',
    ROOT/'claude/runtime/output-validator.md',
]

def test_active_files_exist():
    assert all(p.exists() for p in ACTIVE)
    assert (ROOT/'claude/schemas/SIMS_FEEDBACK_V2.schema.json').exists()
    assert (ROOT/'claude/templates/response-template.md').exists()

def test_active_contract_is_only_4_0():
    text='\n'.join(p.read_text(encoding='utf-8') for p in ACTIVE)
    assert 'contract_version: "2.1"' not in text
    assert 'contract_version: "3.0"' not in text
    assert '`contract_version`: `4.0`' in text or 'contract_version`が`4.0' in text

def test_schema_is_contract_4_0_minimal():
    schema=json.loads((ROOT/'schemas/SIMS_FEEDBACK_V2.schema.json').read_text(encoding='utf-8'))
    assert schema['properties']['contract_version']['const']=='4.1'
    banned={'validation','publication_qa','swls','protected_elements','internal_link_evaluation','coverage_confidence','warnings','changes','new_values'}
    assert not (banned & set(schema['properties']))

def test_evidence_precedence_is_explicit():
    text=(ROOT/'claude/CLAUDE_PROJECT_INSTRUCTIONS.md').read_text(encoding='utf-8')
    assert 'Editorial Strategyは「何を編集するか」だけを決めます' in text
    assert 'MULTIPLE_THIRD_PARTY' in text
    assert '公開OKへ昇格させない' in text

def test_visibility_bans_internal_link_rejection_table():
    text=(ROOT/'claude/runtime/output-validator.md').read_text(encoding='utf-8')
    assert '内部リンク不採用候補の一覧表' in text
    assert 'FAIL' in text
