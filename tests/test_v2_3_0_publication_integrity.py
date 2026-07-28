from pathlib import Path
ROOT=Path(__file__).parents[1]

def test_v23_runtime_and_rules():
    assert (ROOT/'VERSION').read_text().strip()=='2.4.0'
    required=[
      'runtime/publication-integrity-hardening-v2.3.md',
      'runtime/correction-request-mode-v2.3.md',
      'quality/rules/factuality/QF-FAC-005-dynamic-information-freshness.yaml',
      'quality/rules/publication/QF-PUB-005-publication-json-synchronization.yaml',
      'quality/rules/publication/QF-PUB-006-affiliate-cta-validation.yaml',
      'quality/rules/completeness/QF-COM-004-cross-component-claim-sweep.yaml']
    for path in required: assert (ROOT/path).is_file()

def test_output_validator_has_integrity_gate():
    text=(ROOT/'claude/runtime/output-validator.md').read_text()
    for token in ['Publication Integrity Gate v2.3','最安値','CTA','Contract 4.2 JSON']:
      assert token in text
