from __future__ import annotations
from pathlib import Path
import json, sys, datetime
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator
from runtime.sims_writer_runtime.adapters.structured_model import StructuredModelAdapter
from runtime.sims_writer_runtime.adapters.model_protocol import ModelResponse

class CaseTransport:
    provider="golden-fixture"
    def __init__(self, draft): self.draft=draft
    def invoke(self, request):
        return ModelResponse(text=json.dumps(self.draft,ensure_ascii=False),model="golden-fixture-v1",provider=self.provider,usage={"input_units":1,"output_units":1})

def run_case(path:Path):
    case=json.loads(path.read_text(encoding="utf-8"))
    adapter=StructuredModelAdapter(CaseTransport(case["fixture_draft"]),"golden-fixture-v1")
    result=RuntimeOrchestrator(ROOT,adapter=adapter).execute(case["request"],case.get("input_type","generic"))
    expected=case["expected"]; errors=[]
    if result.status != expected["publish_decision"]: errors.append(f"decision expected={expected['publish_decision']} actual={result.status}")
    if result.status != "failed":
        qr=result.artifacts.get("quality_report",{})
        if qr.get("rules_evaluated") != expected["rules_evaluated"]: errors.append("quality rule count mismatch")
        if len(qr.get("gate_results",[])) != expected["gates_evaluated"]: errors.append("quality gate count mismatch")
        package=result.artifacts.get("publication_package",{})
        text=json.dumps(package,ensure_ascii=False)
        for word in expected.get("must_include",[]):
            if word not in text: errors.append(f"missing required text: {word}")
        for word in expected.get("must_not_include",[]):
            if word in text: errors.append(f"forbidden text remains: {word}")
    return {"id":case["id"],"status":"pass" if not errors else "fail","expected":expected["publish_decision"],"actual":result.status,"errors":errors}

def main():
    manifest=json.loads((ROOT/"tests/golden/manifest.json").read_text(encoding="utf-8"))
    results=[run_case(ROOT/item["path"]) for item in manifest["cases"]]
    report={"dataset_version":manifest["dataset_version"],"executed_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"total":len(results),"passed":sum(r["status"]=="pass" for r in results),"failed":sum(r["status"]=="fail" for r in results),"results":results}
    out=ROOT/"tests/golden/reports/latest-report.json"; out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    for r in results: print(f"{r['status'].upper():4} {r['id']} expected={r['expected']} actual={r['actual']}" + (f" :: {'; '.join(r['errors'])}" if r['errors'] else ""))
    print(f"Golden UAT: {report['passed']}/{report['total']} passed")
    if report["failed"]: raise SystemExit(1)
if __name__=="__main__": main()
