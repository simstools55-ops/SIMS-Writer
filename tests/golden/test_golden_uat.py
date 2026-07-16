from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
r=subprocess.run([sys.executable,str(ROOT/'tools/uat/run_golden_uat.py')],cwd=ROOT)
assert r.returncode==0
print('golden UAT tests: PASS')
