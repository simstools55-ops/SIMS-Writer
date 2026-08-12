from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def test_internal_link_referral_policy_exists_and_is_editorial():
    text=(ROOT/'runtime/internal-link-referral-quality-v3.3.1-rc2.md').read_text(encoding='utf-8')
    for token in ['internal_link_recommendations','final placement','surrounding sentence','anchor wording','Do not mechanically append','max_links']:
        assert token in text

def test_version_rc2():
    assert (ROOT/'VERSION').read_text(encoding='utf-8').strip()=='3.3.2-RC4'
