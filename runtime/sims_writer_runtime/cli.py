import argparse, json
from pathlib import Path
from .orchestrator import RuntimeOrchestrator

def main() -> int:
    parser=argparse.ArgumentParser(description="SIMS Writer Runtime Core dry-run")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--input-type", choices=["generic","sbm"], default="generic")
    args=parser.parse_args()
    input_path=Path(args.input).resolve()
    repo_root=Path(__file__).resolve().parents[2]
    raw=json.loads(input_path.read_text(encoding="utf-8"))
    result=RuntimeOrchestrator(repo_root).execute(raw,args.input_type)
    output=Path(args.output).resolve(); output.mkdir(parents=True,exist_ok=True)
    (output/"runtime-result.json").write_text(json.dumps(result.to_dict(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"status={result.status} execution_id={result.execution_id}")
    return 0 if result.status != "failed" else 1

if __name__ == "__main__": raise SystemExit(main())
