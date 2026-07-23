from pathlib import Path

def test_writer_snapshot_excludes_creator_mapping():
    root=Path(__file__).resolve().parents[1]
    for s in [root/'shared',root/'claude'/'shared']:
        assert not (s/'mappings'/'article-creator').exists()
        assert (s/'mappings'/'writer').exists()
        assert 'writer' in (s/'SNAPSHOT_SCOPE.json').read_text(encoding='utf-8')

def test_writer_identity_lock():
    root=Path(__file__).resolve().parents[1]
    t=(root/'claude'/'CLAUDE_PROJECT_INSTRUCTIONS.md').read_text(encoding='utf-8')
    assert 'Do not present Creator-versus-Writer A/B choices' in t
