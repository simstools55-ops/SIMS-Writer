from runtime.sims_writer_runtime.hotfix_validation import validate_hotfix

def test_rejects_v1():
    p={"feedback":{"format":"SIMS_FEEDBACK_V1","version":"1.1"}}
    assert "VAL-JSON-001" in validate_hotfix(p)

def test_rejects_raw_html():
    p={"feedback":{"format":"SIMS_FEEDBACK_V2","version":"2.0"},"rendered_response":"<div style=\"x\"><pre>text</pre></div>"}
    assert "VAL-PRESENTATION-001" in validate_hotfix(p)

def test_detects_id_mismatch():
    p={"input_article_id":"A1","input_article_url":"https://a.example/1","feedback":{"format":"SIMS_FEEDBACK_V2","version":"2.0","article_id":"A2","article_url":"https://a.example/1"}}
    assert "VAL-ID-001" in validate_hotfix(p)

def test_detects_answer_conflict():
    p={"feedback":{"format":"SIMS_FEEDBACK_V2","version":"2.0"},"canonical_answers":["翡翠グリーン","黄金の昇り龍"]}
    assert "VAL-ANSWER-001" in validate_hotfix(p)

def test_accepts_wrapped_markdown():
    p={"feedback":{"format":"SIMS_FEEDBACK_V2","version":"2.0"},"rendered_response":"### Before\n\n> long prose wraps naturally\n\n### After\n\n> revised prose"}
    assert validate_hotfix(p)==[]
