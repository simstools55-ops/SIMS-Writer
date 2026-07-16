import argparse
import json
from pathlib import Path

from .orchestrator import RuntimeOrchestrator
from .export import ArtifactRollbackError, ArtifactRollbackManager, ResultArtifactWriter


def main() -> int:
    parser = argparse.ArgumentParser(description="SIMS Writer Runtime Core")
    parser.add_argument("--input")
    parser.add_argument("--output", required=True)
    parser.add_argument("--input-type", choices=["auto", "generic", "sbm"], default="auto")
    parser.add_argument("--rollback-execution-id")
    args = parser.parse_args()

    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)

    if args.rollback_execution_id:
        try:
            manifest = ArtifactRollbackManager().rollback(output, args.rollback_execution_id)
        except ArtifactRollbackError as exc:
            print(f"rollback_failed={exc}")
            return 2
        print(
            "rollback_completed="
            f"{manifest['target_execution_id']} release_ready={str(manifest['release_ready']).lower()}"
        )
        return 0 if manifest.get("release_ready") else 1

    if not args.input:
        parser.error("--input is required unless --rollback-execution-id is used")

    input_path = Path(args.input).resolve()
    repo_root = Path(__file__).resolve().parents[2]
    raw = json.loads(input_path.read_text(encoding="utf-8"))
    result = RuntimeOrchestrator(repo_root).execute(raw, args.input_type)
    ResultArtifactWriter().write(result, output)
    print(f"status={result.status} execution_id={result.execution_id}")
    return 0 if result.status != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
