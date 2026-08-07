from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_rc2_version_and_policy():
    assert (ROOT/'VERSION').read_text(encoding='utf-8').strip()=='3.3.2-RC2'
    text=(ROOT/'CLAUDE_PROJECT_INSTRUCTIONS.md').read_text(encoding='utf-8')
    assert 'internal_link_recommendations' in text
    assert '機械的に列挙してはならない' in text
    assert 'アンカーテキスト' in text
