from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_seven_capability_knowledge_files_exist():
    required = {
        "intent-analysis.md",
        "hidden-anxiety.md",
        "serp-entity-preservation.md",
        "internal-link-semantics.md",
        "faq-evolution.md",
        "conditional-editorial-opinion.md",
        "evidence-transparency.md",
    }
    assert required <= {p.name for p in (ROOT / "knowledge").glob("*.md")}


def test_guardrails_remain_explicit():
    faq = (ROOT / "knowledge/faq-evolution.md").read_text(encoding="utf-8")
    opinion = (ROOT / "knowledge/conditional-editorial-opinion.md").read_text(encoding="utf-8")
    for text in (faq, opinion):
        assert "Change Budget" in text
        assert "Rewrite" in text
        assert "JSON Contract" in text
