from runtime.sims_writer_runtime.final_quality_gates import (
    validate_scope_alignment, validate_device_paths, validate_internal_link_overlap
)

def test_title_cannot_expand_into_excluded_black_screen_intent():
    issues=validate_scope_alignment(title="インスタの背景・画面が勝手に黒くなる直し方", out_of_scope=["画面が勝手に黒くなる"])
    assert any(i.code=="VAL-SCOPE-ALIGNMENT-001" for i in issues)

def test_narrow_background_title_passes_scope_gate():
    assert not validate_scope_alignment(title="インスタの背景が勝手に黒くなる原因と白に戻す方法", out_of_scope=["画面が真っ黒になる"])

def test_unqualified_android_path_is_blocked():
    issues=validate_device_paths(public_text="Androidの場合：設定＞ユーザー補助＞テキストと表示＞色反転", variable_platforms=["android"])
    assert any(i.code=="VAL-DEVICE-PATH-001" for i in issues)

def test_android_search_guidance_passes():
    text="Androidは機種により項目名が異なるため、設定で『色反転』と検索してください。"
    assert not validate_device_paths(public_text=text, variable_platforms=["android"])

def test_public_internal_link_requires_overlap_review():
    links=[{"decision":"public_ok","role_separation":"unknown","query_overlap":"high","overlap_reviewed":False}]
    assert any(i.code=="VAL-INTERNAL-LINK-OVERLAP-001" for i in validate_internal_link_overlap(links))

def test_distinct_reviewed_internal_link_passes():
    links=[{"decision":"public_ok","role_separation":"distinct","query_overlap":"low","overlap_reviewed":True}]
    assert not validate_internal_link_overlap(links)
