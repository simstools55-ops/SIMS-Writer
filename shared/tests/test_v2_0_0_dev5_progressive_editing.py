from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_progressive_editing_knowledge():
    assert (ROOT/'VERSION').read_text(encoding='utf-8').strip()=='3.5.0'
    text=(ROOT/'knowledge/progressive-editing.md').read_text(encoding='utf-8')
    assert 'component level' in text
    assert 'Partial SERP' in text
