from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_common_validation_assets():
    required=["numeric-consistency.md","evidence-boundary.md","causal-expression-safety.md","logical-consistency.md","html-entity-integrity.md","internal-link-integrity.md"]
    for name in required: assert (ROOT/"knowledge"/name).exists()
    text=(ROOT/"validation"/"common-editorial-validation.md").read_text(encoding="utf-8")
    for code in ["VAL-FACT-001","VAL-EVIDENCE-002","VAL-CAUSAL-001","VAL-CONSISTENCY-001","VAL-ENTITY-001","VAL-LINK-001"]: assert code in text
