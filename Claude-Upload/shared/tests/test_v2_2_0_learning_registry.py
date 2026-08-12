from pathlib import Path
import json
ROOT=Path(__file__).parents[1]

def test_learning_registry_assets_and_version():
    assert (ROOT/'VERSION').read_text().strip()=='3.5.0'
    required=['README.md','LEARNING_REGISTRY.json','LEARNING_INTAKE_TEMPLATE.md','LEARNING_SPRINT_PLAYBOOK.md','DECISION_LOG.md']
    for name in required: assert (ROOT/'learning'/name).is_file()
    reg=json.loads((ROOT/'learning/LEARNING_REGISTRY.json').read_text())
    assert len(reg['allowed_classifications'])==5
    assert 'MAPPING_DEFECT' in reg['allowed_classifications']

def test_snapshot_builder_copies_learning():
    text=(ROOT/'tools/build_scoped_snapshot.py').read_text()
    assert '"learning"' in text
    assert (ROOT/'validation/learning-registry-validation.md').is_file()
