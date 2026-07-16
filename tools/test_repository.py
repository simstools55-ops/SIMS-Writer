#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    [sys.executable, "-m", "pytest"],
    [sys.executable, "tests/contracts/test_contract_examples.py"],
    [sys.executable, "tests/decisions/test_decision_assets.py"],
    [sys.executable, "tests/decisions/test_decision_contracts.py"],
    [sys.executable, "tools/validators/validate_knowledge.py"],
    [sys.executable, "tools/validators/validate_patterns.py"],
    [sys.executable, "tools/validators/validate_quality_rules.py"],
    [sys.executable, "tests/quality-rules/test_quality_assets.py"],
    [sys.executable, "tests/model-adapters/test_model_adapters.py"],
    [sys.executable, "tests/refinement/test_targeted_refinement.py"],
    [sys.executable, "tests/runtime/test_quality_runtime.py"],
    [sys.executable, "tests/runtime/test_runtime_core.py"],
    [sys.executable, "tests/golden/test_golden_uat.py"],
    [sys.executable, "tests/migration/test_sims_core_migration.py"],
]


def main() -> int:
    failures: list[str] = []
    for command in COMMANDS:
        label = " ".join(command[1:])
        print(f"\n=== {label} ===")
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode != 0:
            failures.append(label)
    print(f"\nRepository release gate: {len(COMMANDS) - len(failures)}/{len(COMMANDS)} passed")
    if failures:
        print("Failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
