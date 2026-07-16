from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[2]
required=[
 "runtime/sims_writer_runtime/orchestrator.py", "runtime/sims_writer_runtime/cli.py",
 "runtime/orchestration/stage-state-model.json", "runtime/manifests/runtime-manifest.example.json",
 "architecture/runtime/runtime-core-v1.0.md",
]
missing=[p for p in required if not (ROOT/p).exists()]
if missing:
 print("Missing runtime assets:", *missing, sep="\n- "); sys.exit(1)
state=json.loads((ROOT/"runtime/orchestration/stage-state-model.json").read_text(encoding="utf-8"))
if len(state["states"]) < 8: raise SystemExit("stage states incomplete")
for p in ROOT.rglob("*.json"):
 json.loads(p.read_text(encoding="utf-8"))
print("Runtime asset validation passed")
