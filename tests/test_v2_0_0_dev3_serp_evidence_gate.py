from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_serp_gate_assets_exist():
    for name in [
        "serp-evidence-gate-v2.0.md",
        "user-output-compactness-v2.0.md",
    ]:
        assert (ROOT / "runtime" / name).exists()

def test_unverified_serp_is_blocking_not_warning():
    text=(ROOT/'runtime/serp-analysis-engine-v2.0.md').read_text(encoding='utf-8')
    assert 'blocking prerequisite' in text
    assert 'new FAQ entries' in text
    assert 'Search Console query rows' in text
    assert 'return no publication change' in text

def test_planner_rejects_query_only_expansion():
    text=(ROOT/'runtime/editorial-planner-v2.0.md').read_text(encoding='utf-8')
    assert 'cannot alone authorize content expansion' in text
    assert 'INTERNAL_REJECT' in text

def test_claude_instructions_lock_contradiction():
    text=(ROOT/'claude/CLAUDE_PROJECT_INSTRUCTIONS.md').read_text(encoding='utf-8')
    assert 'SERP Evidence Gate v2.1' in text
    assert 'publication-blocking contradiction' in text

def test_internal_audit_has_serp_gate():
    text=(ROOT/'schemas/SIMS_WRITER_INTERNAL_AUDIT_V1.schema.json').read_text(encoding='utf-8')
    assert 'serp_evidence_gate' in text
    assert 'usable_result_count' in text
