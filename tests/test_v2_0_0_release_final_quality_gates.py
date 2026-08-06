from runtime.sims_writer_runtime.final_quality_gates import (
    validate_title_semantics,
    validate_expectation_alignment,
    validate_ymyl_safety,
)


def test_numeric_limit_cannot_be_increased_as_direct_object():
    issues = validate_title_semantics("LINEアルバムの上限は何枚？写真1000枚を増やす5つの対処法")
    assert any(i.code == "VAL-TITLE-SEMANTIC-001" for i in issues)


def test_natural_limit_title_passes():
    assert not validate_title_semantics("LINEアルバムの上限は何枚？追加できない時の対処法5選")


def test_missing_title_promise_blocks():
    issues = validate_expectation_alignment(
        promises=["賃貸OK", "体験談3選"],
        supported_promises=["発売時期"],
    )
    assert any(i.code == "VAL-EXPECTATION-001" for i in issues)


def test_health_adequacy_claim_requires_evidence():
    issues = validate_ymyl_safety(
        domain="health",
        public_text="1日10分で十分です。",
        safety_notes=["無理のない範囲で始める"],
        evidence_level="MULTIPLE_THIRD_PARTY",
    )
    assert any(i.code == "VAL-BENEFIT-CLAIM-001" for i in issues)


def test_high_impact_health_content_requires_safety_note():
    issues = validate_ymyl_safety(
        domain="health",
        public_text="シニア向け縄跳びを紹介します。",
        safety_notes=[],
        evidence_level="OFFICIAL",
    )
    assert any(i.code == "VAL-YMYL-SAFETY-001" for i in issues)


def test_safe_health_wording_passes():
    issues = validate_ymyl_safety(
        domain="health",
        public_text="縄跳びは短時間から始めましょう。膝や腰に不安がある方は医師に相談してください。",
        safety_notes=["無理のない範囲で行う"],
        evidence_level="OFFICIAL",
    )
    assert not issues
