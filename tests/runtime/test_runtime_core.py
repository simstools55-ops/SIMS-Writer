from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator

def main():
    raw=json.loads((ROOT/"examples/runtime/generic-request.json").read_text(encoding="utf-8"))
    result=RuntimeOrchestrator(ROOT).execute(raw)
    assert result.status == "manual_review_required"
    assert len(result.stages) == 11
    assert result.artifacts["publication_package"]["publish_decision"] == "manual_review_required"
    assert result.manifest["asset_lock"]["patterns"] == 61
    assert result.manifest["asset_lock"]["decisions"] == 12
    bad=RuntimeOrchestrator(ROOT).execute({"request_id":"BAD"})
    assert bad.status == "failed"
    print("Runtime core tests passed")
if __name__ == "__main__": main()
