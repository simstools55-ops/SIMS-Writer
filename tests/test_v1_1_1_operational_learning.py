from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_version(): assert (ROOT/"VERSION").read_text().strip()=="1.1.2"
def test_new_rules():
 for p in ["knowledge/operations/KN-OPS-012-canonical-feedback-output.md","knowledge/operations/KN-OPS-013-confidence-and-low-sample.md","knowledge/seo/KN-SEO-009-existing-content-reflection.md","knowledge/factuality/KN-FAC-006-source-scope-and-central-claim.md"]: assert (ROOT/p).is_file()
def test_shared_snapshot(): assert (ROOT/"shared/VERSION").read_text().strip()==(ROOT/"VERSION").read_text().strip()
