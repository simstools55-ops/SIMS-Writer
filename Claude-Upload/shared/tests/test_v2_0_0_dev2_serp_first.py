from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_serp_first_knowledge_exists():
    p=ROOT/'knowledge/serp-first-editorial-planning.md'
    t=p.read_text(encoding='utf-8')
    assert 'not within the top three' in t
    assert 'Never manufacture findings' in t
