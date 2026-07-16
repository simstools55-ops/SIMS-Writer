#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys
root=Path(__file__).resolve().parents[2]
r=subprocess.run([sys.executable,str(root/'tools/validators/validate_decisions.py')],cwd=root)
if r.returncode: raise SystemExit(r.returncode)
reg=json.loads((root/'decision/registry/decision-registry.json').read_text(encoding='utf-8'))
assert len(reg['decisions'])==12
assert (root/'decisions/ADR-0009-decision-layer-between-knowledge-and-pattern.md').exists()
print('Decision asset tests: PASS')
