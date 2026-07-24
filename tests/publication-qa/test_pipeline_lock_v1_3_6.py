from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]

def test_project_instructions_no_contract_20_conflict():
    text=(ROOT/'claude/CLAUDE_PROJECT_INSTRUCTIONS.md').read_text(encoding='utf-8')
    assert 'JSON block, version `2.0`' not in text
    assert 'v1.3.6 Mandatory Publication Pipeline Lock' in text

def test_publication_qa_schema_shape():
    schema=json.loads((ROOT/'contracts/json/SIMS_FEEDBACK_V2.schema.json').read_text(encoding='utf-8'))
    qa=schema['properties']['publication_qa']
    assert {'initial_verdict','final_verdict','review_trace','unresolved_findings'} <= set(qa['required'])

def test_final_output_rejects_qa_label_substitute():
    text=(ROOT/'claude/FINAL_OUTPUT_INTEGRATION_INSTRUCTIONS.md').read_text(encoding='utf-8')
    assert 'standalone `qa_verdict`' in text
