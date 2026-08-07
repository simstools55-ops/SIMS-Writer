from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_versions():
    assert (ROOT/'VERSION').read_text(encoding='utf-8').strip()=='3.3.2-RC2'
    assert (ROOT/'SHARED_VERSION').read_text(encoding='utf-8').strip()=='3.5.0'

def test_instructions_require_doctor_before_after_and_hide_machine_terms():
    text=(ROOT/'CLAUDE_PROJECT_INSTRUCTIONS.md').read_text(encoding='utf-8')
    assert 'Doctor Referralでも' in text
    assert 'Before/Afterを本文表示から省略してはならない' in text
    assert 'allowed_scope' in text
    assert '表示しない' in text

def test_response_template_has_copy_ready_five_fields():
    text=(ROOT/'templates/response-template.md').read_text(encoding='utf-8')
    for token in ['**Before**','**After**','**理由**','**期待する効果**','（該当箇所なし・新規追加）']:
        assert token in text
