from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]

def test_v3_assets_exist():
    required = [
        'knowledge/temporal-search-intent.md','knowledge/content-lifecycle.md',
        'knowledge/evidence-confidence-and-contradiction.md','knowledge/preservation-signals.md',
        'policies/confidence-policy.md','registries/platform-registry.json',
        'patterns/temporal-lifecycle-recovery-pattern.md','validation/temporal-lifecycle-validation.md'
    ]
    for item in required:
        assert (ROOT/item).exists(), item

def test_registry_version():
    data=json.loads((ROOT/'registries/platform-registry.json').read_text(encoding='utf-8'))
    assert data['version']=='3.5.0'
