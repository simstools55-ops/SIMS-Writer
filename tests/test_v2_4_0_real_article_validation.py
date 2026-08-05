from pathlib import Path
ROOT=Path(__file__).parents[1]
def test_v240_runtime_and_snapshot():
 assert (ROOT/'VERSION').read_text().strip()=='3.3.0'
 assert (ROOT/'SHARED_VERSION').read_text().strip()=='3.3.0'
 assert (ROOT/'runtime/real-article-final-gate-v2.4.md').is_file()
 assert (ROOT/'shared/validation/real-article-publication-validation.md').is_file()
 text=(ROOT/'runtime/output-validator.md').read_text()
 assert 'Real Article Final Gate v2.4' in text
