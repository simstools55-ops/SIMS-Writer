from runtime.sims_writer_runtime.final_quality_gates import (
    validate_natural_japanese, validate_similarity_candidate_wording
)


def test_compressed_line_album_title_is_blocked():
    issues = validate_natural_japanese(title="LINEアルバム上限は1000枚｜容量不足を解決")
    assert any(i.code == "VAL-NATURAL-JAPANESE-001" for i in issues)


def test_natural_line_album_title_passes():
    assert not validate_natural_japanese(title="LINEアルバムの上限は1000枚｜容量不足を解決")


def test_vague_similarity_wording_is_blocked():
    issues = validate_similarity_candidate_wording(
        detected=True, user_message="自サイト内に酷似テーマの記事が存在する可能性があります。"
    )
    assert any(i.code == "VAL-SIMILARITY-WORDING-001" for i in issues)


def test_detection_and_user_boundary_passes():
    text = "類似記事候補を検出しました。統合・差別化の最終判断は利用者判断です。"
    assert not validate_similarity_candidate_wording(detected=True, user_message=text)
