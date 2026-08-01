from pathlib import Path
ROOT=Path(__file__).parents[1]

def test_v210_and_snapshot():
    assert (ROOT/'VERSION').read_text().strip()=='3.0.1'
    assert (ROOT/'shared/quality/QUALITY_PATTERN_LIBRARY.md').is_file()
    assert 'No-Loop Rule' in (ROOT/'shared/quality/QUALITY_PATTERN_LIBRARY.md').read_text()
    assert (ROOT/'runtime/quality-pattern-library-application-v2.1.md').is_file()
