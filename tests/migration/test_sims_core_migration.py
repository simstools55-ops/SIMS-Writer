import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
r=subprocess.run([sys.executable,str(ROOT/'tools/migration/validate_sims_core_migration.py')],capture_output=True,text=True)
print(r.stdout)
assert r.returncode==0, r.stderr
assert 'SIMS-Core assets: 10' in r.stdout
assert 'Lessons learned: 12' in r.stdout
