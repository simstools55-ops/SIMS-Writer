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
    args=ap.parse_args()
    raw=json.loads(args.input.read_text(encoding="utf-8"))
    s=CTRImprovementSlice(); req=s.normalize(raw); dec=s.decide(req); draft=s.build_draft(req,dec)
    qe=QualityValidationEngine(args.repo_root)
    ctx={"main_query":req["main_query"],"model_assisted_checks":draft["model_assisted_checks"],"sources":draft.get("citations",[])}
    report=qe.evaluate(draft,ctx)
    refined=TargetedRefinementEngine(qe).refine(draft,report,ctx)
    out={"request":req,"decision":dec.__dict__,"pattern_selection":draft["slice_metadata"]["patterns"],"content_draft":refined["revised_draft"],"quality_report":refined["quality_report"],"publication_package":{"publish_decision":refined["quality_report"]["publish_recommendation"],"seo_title":refined["revised_draft"]["seo_title"],"meta_description":refined["revised_draft"]["meta_description"],"h1":refined["revised_draft"]["h1"],"article_content":refined["revised_draft"]["article_content"],"before_after":{"before_title":req.get("seo_title") or req.get("current_title"),"after_title":refined["revised_draft"]["seo_title"]},"change_reason":dec.reason}}
    text=json.dumps(out,ensure_ascii=False,indent=2)
    if args.output: args.output.write_text(text+"\n",encoding="utf-8")
    else: print(text)
if __name__=="__main__": main()
