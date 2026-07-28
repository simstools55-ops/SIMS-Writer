from pathlib import Path
import json
ROOT=Path(__file__).parents[1]

def test_learning_registry_reaches_writer_snapshot():
    assert (ROOT/'VERSION').read_text().strip()=='2.4.0'
    assert (ROOT/'shared/learning/LEARNING_REGISTRY.json').is_file()
    reg=json.loads((ROOT/'shared/learning/LEARNING_REGISTRY.json').read_text())
    assert 'PREFERENCE_ONLY' in reg['allowed_classifications']
    assert (ROOT/'runtime/learning-registry-application-v2.2.md').is_file()
