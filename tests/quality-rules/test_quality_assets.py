from pathlib import Path
import subprocess, sys

def test_quality_assets():
 root=Path(__file__).resolve().parents[2]
 subprocess.run([sys.executable, str(root/'tools/validators/validate_quality_rules.py')], check=True)
