from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_version(): assert (ROOT/'VERSION').read_text().strip()=='3.5.0'
def test_four_layers():
 for d in ('knowledge','strategy','evidence','patterns'):
  assert (ROOT/d).is_dir() and any((ROOT/d).iterdir())
def test_strategy_validation(): assert (ROOT/'validation/editorial-strategy-validation.md').exists()
