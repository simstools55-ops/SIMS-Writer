from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
INSTRUCTIONS = (ROOT / "claude/CLAUDE_PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")
KNOWLEDGE = (ROOT / "claude/knowledge/SIMS_WRITER_KNOWLEDGE_PACK.md").read_text(encoding="utf-8")


def declared_version(text: str) -> str:
    match = re.search(r"^Version:\s*(\S+)", text, re.MULTILINE)
    assert match, "Version header is missing"
    return match.group(1)


def test_versions_are_aligned():
    assert declared_version(INSTRUCTIONS) == VERSION
    assert declared_version(KNOWLEDGE) == VERSION


def test_explainable_degradation_fields_exist_in_both_assets():
    for field in ("main_query_source", "execution_mode", "estimated_fields", "information"):
        assert field in INSTRUCTIONS
        assert field in KNOWLEDGE


def test_old_feedback_contract_is_migrated_unless_strictly_fixed():
    assert "v1.2へ自動移行" in INSTRUCTIONS
    assert "旧契約からの自動移行" in KNOWLEDGE
    assert "v1.1固定" in INSTRUCTIONS


def test_estimation_and_catalog_skip_are_not_warnings():
    assert '説明は`information`へ記録する' in KNOWLEDGE
    assert '原則として`warnings`ではなく`information`へ入れる' in KNOWLEDGE


def test_body_flag_rule_is_explicit():
    assert '`changes.body=false`' in KNOWLEDGE


def test_confirmation_items_do_not_duplicate_information():
    assert "確認事項がなければ見出しごと省略" in INSTRUCTIONS
    assert "単なる言い換え" in INSTRUCTIONS
    assert "確認事項が0件なら" in KNOWLEDGE


def test_primary_and_secondary_intent_rule_is_explicit():
    assert "副次意図" in INSTRUCTIONS
    assert "Primary" in KNOWLEDGE and "Secondary" in KNOWLEDGE


def test_expected_effect_does_not_invent_ranking_gain():
    assert "順位改善" in INSTRUCTIONS
    assert "直接根拠のない順位改善" in KNOWLEDGE
