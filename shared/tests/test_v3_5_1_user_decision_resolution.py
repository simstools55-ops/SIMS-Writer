from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_user_decision_resolution_policy_present():
    text=(ROOT/'policies/user-decision-resolution-policy-v3.5.1.md').read_text(encoding='utf-8')
    assert 'USER_DECISION' in text
    assert 'Weak evidence alone is not a user decision' in text
    assert 'YES / NO' in text

def test_editorial_visibility_limits_user_decision():
    text=(ROOT/'knowledge/editorial-decision-and-visibility.md').read_text(encoding='utf-8')
    assert '利用者だけが確定できる' in text
    assert '弱いEvidence' in text
