from pathlib import Path
ROOT=Path(__file__).parents[1]

def test_publication_integrity_assets_and_version():
    assert (ROOT/'VERSION').read_text().strip()=='3.5.0'
    required=[
      'knowledge/publication-integrity-and-dynamic-information.md',
      'knowledge/affiliate-cta-boundary.md',
      'knowledge/faq-publication-consistency.md',
      'quality/PUBLICATION_INTEGRITY_STANDARD_V2_3.md',
      'validation/publication-integrity-validation.md',
      'patterns/dynamic-claim-safe-rewrite-pattern.md']
    for path in required: assert (ROOT/path).is_file()

def test_publication_integrity_contains_core_rules():
    text=(ROOT/'validation/publication-integrity-validation.md').read_text()
    for token in ['CTA','FAQ','JSON','最安値','変動情報']:
        assert token in text
