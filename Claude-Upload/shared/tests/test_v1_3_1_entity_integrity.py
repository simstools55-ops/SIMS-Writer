from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_entity_rule_and_version():
    assert (ROOT/"VERSION").read_text(encoding="utf-8").strip()=="3.5.0"
    text=(ROOT/"knowledge/html-entity-integrity.md").read_text(encoding="utf-8")
    for token in ("KN-ENTITY-001","VAL-ENTITY-001","&amp;quot;","メタディスクリプション"):
        assert token in text
