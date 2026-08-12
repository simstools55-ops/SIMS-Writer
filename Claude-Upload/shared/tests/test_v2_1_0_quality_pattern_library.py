from pathlib import Path
ROOT=Path(__file__).parents[1]

def test_version_and_library():
    assert (ROOT/'VERSION').read_text().strip()=='3.5.0'
    lib=(ROOT/'quality/QUALITY_PATTERN_LIBRARY.md').read_text()
    for token in ['QP-004','QP-007','No-Loop Rule','MAPPING_DEFECT','VALIDATION_DEFECT']:
        assert token in lib

def test_registry_sources_exist():
    names=['title-semantic-alignment-pattern.md','expectation-alignment-pattern.md','natural-japanese-pattern.md','evidence-publication-boundary-pattern.md','ymyl-safety-pattern.md','internal-link-role-separation-pattern.md','terminology-unit-consistency-pattern.md','scope-alignment-pattern.md','freshness-qualification-pattern.md']
    for name in names: assert (ROOT/'patterns'/name).is_file()

def test_writer_mapping_connected():
    text=(ROOT/'mappings/writer/application-mapping.md').read_text()
    assert 'Quality Pattern Library' in text and 'MAPPING_DEFECT' in text
