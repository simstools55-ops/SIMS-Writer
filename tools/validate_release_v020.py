#!/usr/bin/env python3
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
required=["VERSION","README.md","CHANGELOG.md","claude/CLAUDE_PROJECT_INSTRUCTIONS.md","contracts/sims-feedback/v2.1/sims-feedback-v2.1.schema.json","runtime/sims_writer_runtime/audit/core.py"]
errors=[]
for p in required:
    f=ROOT/p
    if not f.exists() or f.stat().st_size==0: errors.append(f"missing_or_empty:{p}")
for f in ROOT.rglob("*.json"):
    try: json.loads(f.read_text(encoding="utf-8"))
    except Exception as e: errors.append(f"invalid_json:{f.relative_to(ROOT)}:{e}")
for f in ROOT.rglob("*"):
    if f.is_file():
        try: f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            if f.suffix.lower() not in {".png",".jpg",".jpeg",".gif",".zip",".pyc"}: errors.append(f"non_utf8:{f.relative_to(ROOT)}")
print(json.dumps({"version":(ROOT/'VERSION').read_text().strip(),"errors":errors,"status":"PASS" if not errors else "FAIL"},ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
