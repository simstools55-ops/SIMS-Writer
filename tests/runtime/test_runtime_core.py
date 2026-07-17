from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator

def main():
    raw=json.loads((ROOT/"examples/runtime/generic-request.json").read_text(encoding="utf-8"))
    result=RuntimeOrchestrator(ROOT).execute(raw)
    assert result.status == "revision_required"
    assert len(result.stages) == 11
    assert result.artifacts["publication_package"]["publish_decision"] == "revision_required"
    assert result.manifest["asset_lock"]["patterns"] == 61
    assert result.manifest["asset_lock"]["decisions"] == 12
    bad=RuntimeOrchestrator(ROOT).execute({"request_id":"BAD"})
    assert bad.status == "revision_required"
    assert next(s for s in bad.stages if s.name == "normalization").status == "passed_with_warning"
    assert next(s for s in bad.stages if s.name == "pattern_selection").status == "skipped"
    degraded=RuntimeOrchestrator(ROOT).execute({"request_id":"REQ-DEGRADED","existing_content":"本文"})
    assert degraded.status != "failed"
    assert degraded.artifacts["internal_link_selection"]["status"] == "skipped"
    print("Runtime core tests passed")
if __name__ == "__main__": main()

def test_graceful_degradation_for_missing_optional_inputs():
    result=RuntimeOrchestrator(ROOT).execute({"request_id":"REQ-DEGRADED","existing_content":"本文"})
    assert result.status != "failed"
    normalization=next(s for s in result.stages if s.name=="normalization")
    patterns=next(s for s in result.stages if s.name=="pattern_selection")
    assert normalization.status == "passed_with_warning"
    assert patterns.status == "skipped"
    assert result.artifacts["internal_link_selection"]["status"] == "skipped"
