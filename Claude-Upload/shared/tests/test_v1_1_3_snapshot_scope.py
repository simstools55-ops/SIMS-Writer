from pathlib import Path

def test_snapshot_policy_exists():
    root=Path(__file__).resolve().parents[1]
    text=(root/'docs'/'product-scoped-snapshot-policy.md').read_text(encoding='utf-8')
    assert 'mappings/article-creator/' in text
    assert 'mappings/writer/' in text
    assert (root/'tools'/'build_scoped_snapshot.py').exists()
