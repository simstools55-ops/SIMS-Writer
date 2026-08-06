from runtime.sims_writer_runtime.final_quality_gates import (
    validate_title_semantics, validate_natural_japanese, validate_terminology_consistency
)
from runtime.sims_writer_runtime.editorial_decision import build_publication_result, user_visible_publication_result


def test_capacity_increase_conflicting_with_body_is_blocked():
    issues = validate_title_semantics(
        "LINEアルバムの容量を増やす5つの方法",
        body_text="上限自体を増やすことはできないため、分散保存で対処します。",
    )
    assert any(i.code == "VAL-TITLE-SEMANTIC-003" for i in issues)


def test_natural_japanese_gate_expanded():
    assert validate_natural_japanese(title="Windows11設定を変更する方法")
    assert not validate_natural_japanese(title="Windows 11の設定を変更する方法")


def test_mixed_photo_video_unit_is_blocked():
    issues = validate_terminology_consistency(public_text="写真・動画合わせて最大1,000枚です")
    assert any(i.code == "VAL-TERMINOLOGY-CONSISTENCY-001" for i in issues)


def test_publication_flags_are_independent():
    result = build_publication_result([
        {"component":"seo_title","before":"旧","after":"新"},
        {"component":"faq","before":None,"after":"候補","requires_user_confirmation":True},
    ])
    public = user_visible_publication_result(result)
    assert public["publishable_public_ok_changes"] is True
    assert public["has_user_decision_changes"] is True


def test_no_public_ok_but_user_decision_flags():
    result = build_publication_result([
        {"component":"faq","before":None,"after":"候補","requires_user_confirmation":True},
    ])
    public = user_visible_publication_result(result)
    assert public["publishable_public_ok_changes"] is False
    assert public["has_user_decision_changes"] is True
