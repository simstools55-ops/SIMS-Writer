import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/validators'))
from validate_quality_freeze import validate_semantics

def load(name): return json.loads((ROOT/'tests/quality-freeze/examples'/name).read_text(encoding='utf-8'))
def test_valid_semantics(): assert validate_semantics(load('valid-v2.json')) == []
def test_budget_failure(): assert 'VAL-BUDGET-001' in validate_semantics(load('invalid-budget-v2.json'))
