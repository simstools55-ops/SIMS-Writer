from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_serp_runtime_assets_exist():
    for name in [
        "serp-analysis-engine-v2.0.md",
        "search-intent-model-v2.0.md",
        "gap-analysis-engine-v2.0.md",
        "editorial-planner-v2.0.md",
        "serp-analysis-input-contract-v2.0.md",
    ]:
        assert (ROOT / "runtime" / name).exists()

def test_serp_trigger_and_no_fabrication_are_locked():
    text=(ROOT/'runtime/serp-analysis-engine-v2.0.md').read_text(encoding='utf-8')
    assert 'greater than 3.0' in text
    assert 'top 10' in text
    assert 'Do not fabricate SERP findings' in text

def test_project_instructions_require_serp_before_edits():
    text=(ROOT/'claude/CLAUDE_PROJECT_INSTRUCTIONS.md').read_text(encoding='utf-8')
    assert 'SERP-first Editorial Planning v2.0' in text
    assert 'average position is greater than 3.0' in text
