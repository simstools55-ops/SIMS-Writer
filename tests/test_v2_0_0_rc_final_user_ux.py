from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def read(path): return (ROOT/path).read_text(encoding="utf-8")

def test_version():
    assert read("VERSION").strip()=="2.0.0-rc.3"

def test_status_sentence_and_short_reason():
    text=read("presentation/FEEDBACK_TEMPLATE.md")
    assert "今回の修正は、そのまま公開できます。" in text
    assert "利用者判断の項目だけ確認してください。" in text
    assert "短い一文" in text

def test_internal_link_one_line_only():
    text=read("runtime/user-output-compactness-v2.0.md")
    assert "今回は追加できる内部リンクはありません。" in text
    assert "Do not append candidate counts" in text

def test_validator_has_ux_gate():
    text=read("claude/runtime/output-validator.md")
    assert "## UX Gate" in text
    assert "内部リンク全件不採用時" in text

def test_pipeline_has_ux_filter():
    text=read("claude/runtime/output-pipeline.md")
    assert "UX Filter" in text
