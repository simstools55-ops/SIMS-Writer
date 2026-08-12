from pathlib import Path
ROOT=Path(__file__).parents[1]

def test_version_and_hotfix_knowledge():
    assert (ROOT/'VERSION').read_text().strip()=='3.5.0'
    text=(ROOT/'knowledge/natural-japanese-publication-flags-terminology.md').read_text()
    assert 'publishable_public_ok_changes' in text
    assert 'has_user_decision_changes' in text
    assert 'LINEアルバムの上限' in text
