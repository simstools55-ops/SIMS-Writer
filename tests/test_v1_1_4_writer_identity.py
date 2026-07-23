from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_writer_identity_text():
    t=(ROOT/'claude'/'CLAUDE_PROJECT_INSTRUCTIONS.md').read_text(encoding='utf-8')
    assert 'This project is SIMS Writer' in t
    assert 'existing-article improvement' in t
    assert 'begin the Writer workflow immediately' in t

def test_no_non_writer_mapping():
    assert not (ROOT/'shared'/'mappings'/'article-creator').exists()
    assert not (ROOT/'claude'/'shared'/'mappings'/'article-creator').exists()

def test_reset_files_present():
    assert (ROOT/'claude'/'PROJECT_INSTRUCTIONS_TO_PASTE.md').exists()
    assert (ROOT/'claude'/'PROJECT_RESET_CHECKLIST.md').exists()
