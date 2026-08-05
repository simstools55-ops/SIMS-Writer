from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_shared_serp_gate_is_blocking():
    text=(ROOT/'knowledge/serp-first-editorial-planning.md').read_text(encoding='utf-8')
    assert 'blocking evidence gate' in text
    assert 'Search Console query rows cannot substitute' in text
    assert 'must never both admit' in text
