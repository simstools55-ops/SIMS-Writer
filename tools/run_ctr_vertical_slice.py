from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from runtime.sims_writer_runtime.vertical_slices.ctr_improvement import CTRImprovementSlice
from runtime.sims_writer_runtime.quality.engine import QualityValidationEngine
from runtime.sims_writer_runtime.refinement.engine import TargetedRefinementEngine

def main():
    ap=argparse.ArgumentParser(description="SIMS Writer CTR Improvement Vertical Slice")
    ap.add_argument("input", type=Path)
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--output", type=Path)
    ap.add_argument("--mode", choices=["summary","partial","full","publish","json_only"])
    args=ap.parse_args()
    raw=json.loads(args.input.read_text(encoding="utf-8"))
    if args.mode: raw["output_mode"]=args.mode
    s=CTRImprovementSlice(); req=s.normalize(raw); dec=s.decide(req); draft=s.build_draft(req,dec)
    qe=QualityValidationEngine(args.repo_root)
    ctx={"main_query":req["main_query"],"model_assisted_checks":draft["model_assisted_checks"],"sources":draft.get("citations",[])}
    report=qe.evaluate(draft,ctx)
    refined=TargetedRefinementEngine(qe).refine(draft,report,ctx)
    output_package=s.build_output(req,dec,refined["revised_draft"])
    out={"request":req,"decision":dec.__dict__,"pattern_selection":draft["slice_metadata"]["patterns"],"quality_report":refined["quality_report"],"publication_package":output_package}
    text=json.dumps(out,ensure_ascii=False,indent=2)
    if args.output: args.output.write_text(text+"\n",encoding="utf-8")
    else: print(text)
if __name__=="__main__": main()
