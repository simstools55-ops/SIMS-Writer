from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_version(): assert (ROOT/"VERSION").read_text().strip()=="3.5.0"
def test_gates_documented():
 t=(ROOT/"validation/release-final-quality-gates.md").read_text()
 for code in ["VAL-SCOPE-ALIGNMENT-001","VAL-DEVICE-PATH-001","VAL-INTERNAL-LINK-OVERLAP-001"]: assert code in t
def test_knowledge_file(): assert (ROOT/"knowledge/scope-device-link-release-safety.md").exists()
